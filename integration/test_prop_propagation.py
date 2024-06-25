"""Integration tests for propagation of properties from rendering functions to HTML."""

from typing import Any, Callable, Generator

import pytest
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys

from reflex.components.component import Component
from reflex.components.radix.themes.components import scroll_area
from reflex.components.tags import tag
from reflex.testing import AppHarness
import time


def PropPropagationApp():
    """App using all components for validation."""
    import reflex as rx
    from datetime import datetime, timezone
    from typing import Callable, Any
    from reflex.components.component import Component

    columns: list[dict[str, str]] = [
        {
            "title": "Code",
            "type": "str",
        },
    ]
    data: list[list[Any]] = [
        ["A"],
    ]

    class State(rx.State):
        text: str = "initial"
        date_now: datetime = datetime.now(timezone.utc)

    app = rx.App(state=rx.State)

    test_component_tuple: list[tuple[Callable[[Any], Component], dict[str, Any]]] = []

    def wc(
        comp: Callable[[Any], Component],
        *children: Any | Component | list[Component],
        **kwargs,
    ) -> Component:
        test_component_tuple.append(
            (
                comp,
                kwargs,
            )
        )
        return comp(*children, **kwargs)

    def wcb(
        comp: Callable[[Any], Component],
        *children: Any | Component | list[Component],
        **kwargs,
    ) -> Component:
        return comp(*children, **kwargs)

    @app.add_page
    def index():
        return rx.fragment(
            rx.input(
                value=State.router.session.client_token, is_read_only=True, id="token"
            ),
            wc(
                rx.table.root,
                wc(
                    rx.table.header,
                    wc(
                        rx.table.row,
                        wc(
                            rx.table.column_header_cell,
                            "Column Header",
                            id="test-table-column-header-cell",
                        ),
                        id="test-table-header",
                    ),
                    id="test-table-header-row",
                ),
                wc(
                    rx.table.body,
                    wc(
                        rx.table.row,
                        wc(
                            rx.table.row_header_cell, "Row Header", id="row-header-cell"
                        ),
                        wc(rx.table.cell, "Row 1, Column 1", id="row-1-col-1"),
                        id="test-table-row",
                    ),
                    id="test-table-body",
                ),
                id="test-table",
            ),
            wc(rx.icon, tag="pencil", id="icon"),
            rx.debounce_input(
                wc(
                    rx.input,
                    on_change=lambda e: rx.redirect(e),
                    id="input-inside-debounce",
                )
            ),
            wc(
                rx.callout,
                "You will need admin privileges to install and access this application.",
                icon="info",
                id="callout",
            ),
            wc(
                rx.code_block,
                """def fib(n):
                if n <= 1:
                    return n
                else:
                    return(fib(n-1) + fib(n-2))""",
                language="python",
                show_line_numbers=True,
                id="codeblock",
            ),
            wcb(rx.avatar, src="/logo.jpg", id="avatar"),
            wcb(rx.data_editor, columns=columns, data=data, id="data-editor"),
            wc(rx.flex, id="flex"),
            wc(
                rx.list.ordered, wc(rx.list.item, "Item1", id="olist-item1"), id="olist"
            ),
            wc(
                rx.list.unordered,
                wc(rx.list.item, "Item1", id="ulist-item1"),
                id="ulist",
            ),
            wcb(rx.moment, State.date_now, id="one-moment"),
            wc(rx.progress, value=50, id="progress-50-percent"),
            wc(rx.scroll_area, id="scrollarea"),
            wc(rx.spinner, id="spinner"),
            wc(
                rx.accordion.root,
                wc(
                    rx.accordion.item,
                    header="First Item",
                    content="The first accordion item's content",
                    id="accordeon-item",
                ),
                width="300px",
                id="accordeon",
            ),
            wc(
                rx.tabs.root,
                wc(
                    rx.tabs.list,
                    wc(rx.tabs.trigger, "Tab 1", value="tab1", id="tabs-trigger-1"),
                    id="tabs-list",
                ),
                wc(
                    rx.tabs.content,
                    rx.text("item on tab 1"),
                    value="tab1",
                    id="tabs-content-1",
                ),
                id="tabs",
            ),
            wc(
                rx.form,
                wc(rx.button, "Some button", id="button"),
                wc(
                    rx.checkbox,
                    "Agree to Terms and Conditions",
                    default_checked=True,
                    spacing="2",
                    id="checkbox",
                ),
                wcb(rx.editor, id="editor"),
                wc(rx.input, id="test-input"),
                wc(rx.radio, ["1", "2", "3"], default_value="1", id="radio"),
                wcb(
                    rx.select,
                    ["Apple", "Orange", "Banana", "Grape", "Pear"],
                    id="select",
                ),
                wc(rx.slider, default_value=40, id="slider"),
                wc(rx.switch, default_checked=True, id="switch"),
                wc(rx.text_area, place_holder="type here...", id="textarea"),
                wc(rx.upload, id="upload"),

                id="form",
            ),
        )

    app.test_component_tuple = test_component_tuple


@pytest.fixture()
def prop_propagation_harness(tmp_path) -> Generator[AppHarness, None, None]:
    """Start FullyControlledInput app at tmp_path via AppHarness.

    Args:
        tmp_path: pytest tmp_path fixture

    Yields:
        running AppHarness instance
    """
    with AppHarness.create(
        root=tmp_path,
        app_source=PropPropagationApp,  # type: ignore
    ) as harness:
        yield harness


@pytest.mark.asyncio
async def test_prop_propagation(prop_propagation_harness: AppHarness):
    """Type text after moving cursor. Update text on backend.

    Args:
        fully_controlled_input: harness for FullyControlledInput app
    """
    assert prop_propagation_harness.app_instance is not None, "app is not running"
    driver = prop_propagation_harness.frontend()

    # get a reference to the connected client
    token_input = driver.find_element(By.ID, "token")
    assert token_input

    assert prop_propagation_harness.app_instance is not None

    for test_component in prop_propagation_harness.app_instance.test_component_tuple:
        id: str = test_component[1].get("id", None)
        if id is not None:
            element = driver.find_element(By.ID, id)

            assert element is not None

            print(f"Found element with id {id}")
            # for key in test_component[1].keys():
            #     if key in ["tag", "on_change"]:
            #         continue
            #     assert (
            #         element.get_attribute(key) == test_component[1].get(key)
            #         or element.get_property(key) == test_component[1].get(key)
            #     )
        else:
            assert False, "Expected id in kwargs"


#    time.sleep(100)
