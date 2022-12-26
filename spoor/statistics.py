from collections import UserList

from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table


class TopCalls(UserList):
    def __rich_console__(
        self, 
        console: Console, 
        options: ConsoleOptions,
    ) -> RenderResult:
        # TODO: add hash column?
        # TODO: add id column?
        table = Table("#", "Name", "Called", "Call count")
        for index, entry in enumerate(self.data, start=1):
            call_count = entry[1]
            table.add_row(
                f"{index}", 
                f"[bold magenta]{entry[0]}[/]", 
                "[green]yes[/]" if call_count else "[yellow]no[/]", 
                f"{call_count}",
            )
        yield table


if __name__ == "__main__":
    from rich import print as rprint
    tc = TopCalls()
    rprint(tc)
    print(tc)
