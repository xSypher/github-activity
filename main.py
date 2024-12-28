from argparse import ArgumentParser as parser
import functions as func


def start_cli() -> None:

    cli = parser(prog="github-activity",
                    description="Show the github user's activity in terminal",
                    usage="github-activity <user>",
                    )
    cli.add_argument("user", help="user's name", type=str)
    args = cli.parse_args()

    events = func.get_activity(args.user)
    events = func.parse_events(events)
    func.print_events(events)

if __name__ == "__main__":
    start_cli()