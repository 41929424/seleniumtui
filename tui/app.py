from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, RichLog, Select, Static

from tui.progress import read_progress, record_run
from tui.runner import run_pytest


class WorkbenchApp(App):
    TITLE = "SauceDemo QA Workbench"
    SUB_TITLE = "UI regression runner"
    CSS = """
    Screen { padding: 1 2; }
    #intro { height: auto; padding: 1; color: $text; background: $panel; }
    Horizontal { height: 3; margin-top: 1; }
    Select { width: 1fr; }
    Button { margin-left: 1; }
    RichLog { height: 1fr; border: round $accent; margin-top: 1; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static("20 SauceDemo regression scenarios | Python + Selenium + pytest", id="intro")
            yield Static(id="progress")
            with Horizontal():
                yield Select(
                    [
                        ("All test modules", "tests/ui"),
                        ("Authentication", "tests/ui/test_login.py"),
                        ("Product catalog", "tests/ui/test_inventory.py"),
                        ("Cart", "tests/ui/test_cart.py"),
                        ("Checkout", "tests/ui/test_checkout.py"),
                    ],
                    value="tests/ui",
                    id="target",
                    allow_blank=False,
                )
                yield Button("Run tests", variant="primary", id="run")
            yield RichLog(id="output", wrap=True, markup=False)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run":
            output = self.query_one("#output", RichLog)
            target = str(self.query_one("#target", Select).value)
            output.clear()
            output.write("Starting pytest...")
            progress = self.query_one("#progress", Static)
            progress.update("Verification in progress...")
            self.execute_tests(target, output, progress)

    @work(thread=True, exclusive=True)
    def execute_tests(self, target: str, log: RichLog, progress: Static) -> None:
        result = run_pytest(str(target))
        verified_count = record_run(target)
        output = result.stdout + result.stderr
        self.call_from_thread(log.write, output or "pytest returned no output")
        status = "PASSED" if result.returncode == 0 else f"FAILED (exit {result.returncode})"
        self.call_from_thread(log.write, f"\nRun complete: {status}")
        self.call_from_thread(
            progress.update,
            f"Verified scenarios: {verified_count}/20",
        )

    def on_mount(self) -> None:
        self.query_one("#progress", Static).update(
            f"Verified scenarios: {len(read_progress())}/20"
        )


def main() -> None:
    WorkbenchApp().run()


if __name__ == "__main__":
    main()
