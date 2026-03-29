# main.py
import json
from models import Player, Team
import ds_engine

NUM_TEAMS = 7
ROSTER_SIZE = 15
NUM_WEEKS = 14


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


def main():
    all_players = load_players()
    teams = setup_teams()
    db = ds_engine.PlayerDatabase()

    # ── Pre-Game: Draft ──────────────────────────────────────────────────────
    print("\nStarting snake draft...")
    all_players.sort(key=lambda p: p.fantasy_value, reverse=True)
    ds_engine.run_snake_draft(teams, all_players, user_team=teams[0])

    # Build waiver wire from undrafted players
    drafted_ids = {p.id for team in teams for p in team.roster}
    undrafted = [p for p in all_players if p.id not in drafted_ids]
    wire = ds_engine.MaxHeap()
    for p in undrafted:
        wire.insert(p)

    season_schedule = generate_schedule(teams, NUM_WEEKS)

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

    # ── Hub ──────────────────────────────────────────────────────────────────
    while week <= NUM_WEEKS:
        print(f"\n{'='*40}")
        print(f"  TERMINAL HOOPS GM  |  Week {week}")
        print(f"{'='*40}")
        print("[1] View Roster & Stats")
        print("[2] View League Standings")
        print("[3] Waiver Wire")
        print("[4] League Stat Leaders")
        print("[5] View Schedule Network")
        print("[6] Simulate Next Week")
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
                if drop_choice.isdigit():
                    idx = int(drop_choice) - 1
                    dropped = user_team.roster.pop(idx)
                    wire.insert(dropped)
                    user_team.roster.append(top)
                    print(f"Dropped {dropped.name}, added {top.name}.")
                else:
                    wire.insert(top)  # put them back
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
                print(f"  {a.name} {score_a} – {score_b} {b.name}  ({winner.name} wins)")
            if bye_team:
                print(f"  {bye_team.name} — BYE")
            week += 1
            # Rebuild BST with updated win counts
            standings = ds_engine.BST()
            for t in teams:
                standings.insert(t)

        elif choice == "Q":
            print("Thanks for playing Terminal Hoops GM!")
            break


if __name__ == "__main__":
    main()
