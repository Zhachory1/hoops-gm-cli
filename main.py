# main.py
import argparse
import csv
import json
import random
from pathlib import Path
from models import Player, Team
import ds_engine

NUM_TEAMS = 7
ROSTER_SIZE = 15
NUM_WEEKS = 14


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Terminal Hoops GM")
    parser.add_argument("--seed", type=int, default=None, help="random seed for reproducible seasons")
    parser.add_argument("--weeks", type=int, default=NUM_WEEKS, help="number of weeks to simulate")
    parser.add_argument("--save", default=None, help="write league state JSON to this path")
    parser.add_argument("--export-json", default=None, help="write draft/results summary JSON to this path")
    parser.add_argument("--export-csv", default=None, help="write draft/results summary CSV to this path")
    return parser.parse_args(argv)


def load_players() -> list[Player]:
    with open("data/players.json") as f:
        raw = json.load(f)
    return [Player(**p) for p in raw]


def setup_teams() -> list[Team]:
    teams = []
    print("\n=== TERMINAL HOOPS GM ===")
    print("Enter a name for YOUR team:")
    your_name = input("> ").strip() or "My Team"
    teams.append(Team(name=your_name))
    cpu_names = ["Rim Rockers", "Splash Brothers", "Paint Pounders",
                 "Net Ninjas", "Hoop Dreams", "Fast Breaks"]
    for name in cpu_names:
        teams.append(Team(name=name))
    return teams


def claim_waiver_player(user_team: Team, wire: ds_engine.MaxHeap, top: Player, drop_choice: str) -> bool:
    if drop_choice.isdigit():
        idx = int(drop_choice) - 1
        if 0 <= idx < len(user_team.roster):
            dropped = user_team.roster.pop(idx)
            wire.insert(dropped)
            user_team.roster.append(top)
            print(f"Dropped {dropped.name}, added {top.name}.")
            return True
    wire.insert(top)
    print("Invalid roster number; waiver claim cancelled.")
    return False


def player_to_dict(player: Player) -> dict:
    return {
        "id": player.id,
        "name": player.name,
        "points_avg": player.points_avg,
        "assists_avg": player.assists_avg,
        "defense_rating": player.defense_rating,
        "fantasy_value": player.fantasy_value,
    }


def team_to_dict(team: Team) -> dict:
    return {
        "name": team.name,
        "wins": team.wins,
        "losses": team.losses,
        "roster": [player_to_dict(player) for player in team.roster],
    }


def league_state(teams: list[Team], week: int, total_weeks: int, user_team: Team, results: list[dict]) -> dict:
    return {
        "week": week,
        "total_weeks": total_weeks,
        "user_team": user_team.name,
        "teams": [team_to_dict(team) for team in teams],
        "results": results,
    }


def write_json(path: str, payload: dict) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n")


def save_league_state(path: str, teams: list[Team], week: int, total_weeks: int, user_team: Team, results: list[dict]) -> None:
    write_json(path, league_state(teams, week, total_weeks, user_team, results))


def export_summary_json(path: str, teams: list[Team], results: list[dict], user_team: Team) -> None:
    write_json(path, {
        "user_team": user_team.name,
        "draft": [team_to_dict(team) for team in teams],
        "results": results,
    })


def export_summary_csv(path: str, teams: list[Team], results: list[dict]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["section", "team", "player", "week", "opponent", "score", "opponent_score", "winner"])
        writer.writeheader()
        for team in teams:
            for player in team.roster:
                writer.writerow({"section": "draft", "team": team.name, "player": player.name})
        for result in results:
            writer.writerow({
                "section": "result",
                "team": result["team_a"],
                "week": result["week"],
                "opponent": result["team_b"],
                "score": result["score_a"],
                "opponent_score": result["score_b"],
                "winner": result["winner"],
            })


def generate_schedule(teams: list[Team], num_weeks: int) -> list[list[tuple]]:
    """
    Round-robin schedule using the circle algorithm.
    With an odd number of teams, one team gets a bye each week (None slot).
    Returns a list of `num_weeks` rounds; each round is a list of (Team, Team) pairs.
    Repeats the round-robin cycle if num_weeks exceeds the number of rounds.
    """
    pool = teams[:]
    if len(pool) % 2 == 1:
        pool.append(None)  # bye placeholder

    n = len(pool)
    fixed = pool[0]
    rotating = pool[1:]
    rounds = []

    for _ in range(n - 1):
        circle = [fixed] + rotating
        pairs = [
            (circle[i], circle[n - 1 - i])
            for i in range(n // 2)
            if circle[i] is not None and circle[n - 1 - i] is not None
        ]
        rounds.append(pairs)
        rotating = [rotating[-1]] + rotating[:-1]  # rotate right by one

    return [rounds[i % len(rounds)] for i in range(num_weeks)]


def main(argv=None):
    args = parse_args(argv)
    if args.seed is not None:
        random.seed(args.seed)

    all_players = load_players()
    teams = setup_teams()
    db = ds_engine.PlayerDatabase()
    for player in all_players:
        db.load(player)

    # Each CPU team has a unique scoring personality used during auto-picks.
    # Weights reflect how much the team values points vs assists vs defense.
    team_scorers = {
        "Rim Rockers":     lambda p: p.points_avg * 2.0 + p.assists_avg * 0.5 + p.defense_rating * 1.0,
        "Splash Brothers": lambda p: p.points_avg * 1.2 + p.assists_avg * 2.0 + p.defense_rating * 0.3,
        "Paint Pounders":  lambda p: p.points_avg * 0.8 + p.assists_avg * 0.5 + p.defense_rating * 3.0,
        "Net Ninjas":      lambda p: p.points_avg * 1.0 + p.assists_avg * 1.5 + p.defense_rating * 1.5,
        "Hoop Dreams":     lambda p: p.points_avg * 3.0 + p.assists_avg * 0.3 + p.defense_rating * 0.2,
        "Fast Breaks":     lambda p: p.points_avg * 1.0 + p.assists_avg * 2.5 + p.defense_rating * 0.5,
    }

    # ── Pre-Game: Draft ──────────────────────────────────────────────────────
    # Weighted shuffle: higher-FV players tend to appear earlier but aren't
    # locked in place — sigma=8 gives meaningful variance across the pool.
    all_players.sort(key=lambda p: p.fantasy_value + random.gauss(0, 8), reverse=True)
    print("\nStarting snake draft...")
    ds_engine.run_snake_draft(teams, all_players, user_team=teams[0], team_scorers=team_scorers)

    # Build waiver wire from undrafted players
    drafted_ids = {p.id for team in teams for p in team.roster}
    undrafted = [p for p in all_players if p.id not in drafted_ids]
    wire = ds_engine.MaxHeap()
    for p in undrafted:
        wire.insert(p)

    season_schedule = generate_schedule(teams, args.weeks)

    # Build the graph from the actual scheduled matchups
    schedule = ds_engine.ScheduleGraph()
    for weekly_pairs in season_schedule:
        for a, b in weekly_pairs:
            schedule.add_matchup(a.name, b.name)

    week = 1
    standings = ds_engine.BST()
    for t in teams:
        standings.insert(t)

    user_team = teams[0]
    results_log = []

    # ── Hub ──────────────────────────────────────────────────────────────────
    while week <= args.weeks:
        print(f"\n{'='*40}")
        print(f"  TERMINAL HOOPS GM  |  Week {week}")
        print(f"{'='*40}")
        print("[1] View Roster & Stats")
        print("[2] View League Standings")
        print("[3] Waiver Wire")
        print("[4] League Stat Leaders")
        print("[5] View Schedule Network")
        print("[6] Simulate Next Week")
        print("[7] Search Player Database")
        if args.save:
            print("[S] Save Season")
        print("[Q] Quit")
        choice = input("\n> ").strip().upper()

        if choice == "1":
            print(f"\n{user_team.name} Roster ({len(user_team.roster)}/{Team.MAX_ROSTER_SIZE}):")
            for i, p in enumerate(user_team.roster, 1):
                print(f"  {i:2}. {p.name:<25} PTS:{p.points_avg:5.1f}  AST:{p.assists_avg:4.1f}  DEF:{p.defense_rating:4.1f}  FV:{p.fantasy_value:5.1f}")

        elif choice == "2":
            ranked = standings.inorder()
            print("\n── League Standings ──")
            for rank, team in enumerate(ranked, 1):
                print(f"  {rank}. {team.name:<20} {team.wins}W - {team.losses}L")

        elif choice == "3":
            top = wire.extract_max()
            if not top:
                print("Waiver wire is empty.")
                continue
            print(f"\nTop available: {top.name} (FV: {top.fantasy_value:.1f})")
            if len(user_team.roster) >= Team.MAX_ROSTER_SIZE:
                print("Roster full. Type the number of the player to drop, or [C]ancel:")
                for i, p in enumerate(user_team.roster, 1):
                    print(f"  {i}. {p.name} (FV: {p.fantasy_value:.1f})")
                drop_choice = input("> ").strip()
                claim_waiver_player(user_team, wire, top, drop_choice)
            else:
                user_team.roster.append(top)
                print(f"Added {top.name} to your roster!")

        elif choice == "4":
            print("\nSort by: [P]oints  [A]ssists  [D]efense")
            stat_choice = input("> ").strip().upper()
            attr_map = {"P": "points_avg", "A": "assists_avg", "D": "defense_rating"}
            attr = attr_map.get(stat_choice, "points_avg")
            all_rostered = [p for t in teams for p in t.roster]
            sorted_players = ds_engine.merge_sort(all_rostered, attr)
            print(f"\n── Top 50 by {attr} ──")
            for i, p in enumerate(sorted_players[:50], 1):
                print(f"  {i:2}. {p.name:<25} {getattr(p, attr):5.1f}")

        elif choice == "5":
            print(f"\nEnter team name to see their schedule path (DFS):")
            tname = input("> ").strip()
            path = schedule.dfs(tname)
            if path:
                print(" -> ".join(path))
            else:
                print("Team not found.")

        elif choice == "7":
            print("\nEnter a player name:")
            player_name = input("> ").strip()
            player = db.get_player_by_name(player_name)
            if player:
                rostered_by = next((t.name for t in teams if player in t.roster), "Waiver Wire")
                print(
                    f"  {player.name} — PTS:{player.points_avg:.1f} "
                    f"AST:{player.assists_avg:.1f} DEF:{player.defense_rating:.1f} "
                    f"FV:{player.fantasy_value:.1f} ({rostered_by})"
                )
            else:
                print("Player not found.")

        elif choice == "6":
            matchups = season_schedule[week - 1]
            playing_names = {t.name for pair in matchups for t in pair}
            bye_team = next((t for t in teams if t.name not in playing_names), None)
            print(f"\n── Week {week} Results ──")
            for a, b in matchups:
                winner, score_a, score_b = ds_engine.simulate_matchup(a, b)
                loser = b if winner == a else a
                winner.wins += 1
                loser.losses += 1
                results_log.append({
                    "week": week,
                    "team_a": a.name,
                    "team_b": b.name,
                    "score_a": score_a,
                    "score_b": score_b,
                    "winner": winner.name,
                })
                print(f"  {a.name} {score_a} – {score_b} {b.name}  ({winner.name} wins)")
            if bye_team:
                print(f"  {bye_team.name} — BYE")
            week += 1
            # Rebuild BST with updated win counts
            standings = ds_engine.BST()
            for t in teams:
                standings.insert(t)

        elif choice == "S" and args.save:
            save_league_state(args.save, teams, week, args.weeks, user_team, results_log)
            print(f"Saved league state to {args.save}")

        elif choice == "Q":
            print("Thanks for playing Terminal Hoops GM!")
            break

    # ── End Screen (only shown after all weeks complete, not on Q) ────────────
    if week > args.weeks:
        ranked = standings.inorder()
        champion = ranked[0]

        all_rostered = [p for t in teams for p in t.roster]
        mvp = max(all_rostered, key=lambda p: p.fantasy_value)
        mvp_team = next(t for t in teams if mvp in t.roster)

        print(f"\n{'═'*50}")
        print(f"  FINAL STANDINGS — {args.weeks}-WEEK SEASON COMPLETE")
        print(f"{'═'*50}")
        for rank, team in enumerate(ranked, 1):
            marker = " ← YOU" if team is user_team else ""
            crown  = "🏆 " if rank == 1 else f"{rank:2}. "
            print(f"  {crown}{team.name:<22} {team.wins:2}W – {team.losses:2}L{marker}")

        print(f"\n  CHAMPION: {champion.name}")
        if champion is user_team:
            print("  You won the season! Great managing.")
        else:
            print(f"  Better luck next season.")

        print(f"\n  MVP: {mvp.name} ({mvp_team.name})")
        print(f"       PTS {mvp.points_avg:.1f}  AST {mvp.assists_avg:.1f}  DEF {mvp.defense_rating:.1f}")
        print(f"{'═'*50}\n")

    if args.save:
        save_league_state(args.save, teams, week, args.weeks, user_team, results_log)
        print(f"Saved league state to {args.save}")
    if args.export_json:
        export_summary_json(args.export_json, teams, results_log, user_team)
        print(f"Exported summary JSON to {args.export_json}")
    if args.export_csv:
        export_summary_csv(args.export_csv, teams, results_log)
        print(f"Exported summary CSV to {args.export_csv}")


if __name__ == "__main__":
    main()
