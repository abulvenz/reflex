"""Integration tests for propagation of properties from rendering functions to HTML."""

from typing import Generator

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


import reflex
from reflex.components.tags import tag
from reflex.testing import AppHarness
import time


def PropPropagationApp():
    """App using all components for validation."""
    import reflex as rx
    from reflex.components.core.debounce import DebounceInput
    from reflex.components.base.bare import Bare
    from reflex.components.base.meta import Image, Meta, Description, Title

    from reflex.components.component import NoSSRComponent
    from reflex.components.core.banner import ConnectionBanner, ConnectionModal
    from reflex.components.core.foreach import Foreach
    from reflex.components.tags.tag import Tag
    from reflex.components.component import Component
    from reflex.components.el.elements.forms import Button, Input
    from reflex.components.radix.themes.components.dialog import DialogTitle
    from reflex.components.radix.themes.base import RadixThemesComponent
    from reflex.components.radix.themes.base import RadixThemesTriggerComponent

    class State(rx.State):
        text: str = "initial"

    app = rx.App(state=rx.State)

    exclude = [
        Bare,
        # RadixThemesTriggerComponent,
        # DialogTitle,
        ConnectionBanner,
        ConnectionModal,
        Foreach,
        DebounceInput,
        NoSSRComponent,
        Tag,
        Image,
        Meta,
        Description,
        Title,
        "Cond",
        "Match",
        "AppWrap",
        "Icon", rx.components.base, "WebsocketTargetURL", rx.components.base.meta
    ]

    def find_rec(cls, result=[]) -> list[type[Component]]:
        for c in cls.__subclasses__():
            if c not in exclude and c.__qualname__ not in exclude and c.__module__ not in exclude:
                result.append(c)                
                print(f"appending {c}")
            else:
                print(f"skipping {c}")
            find_rec(c, result)

        return result

    test_components = find_rec(Component)

    for compo in test_components:
        print(f"compo: {compo}")

    @app.add_page
    def index():
        return rx.fragment(
            rx.input(
                value=State.router.session.client_token, is_read_only=True, id="token"
            ),
            *[comp.create(id=f"id-{comp.__qualname__}") for comp in test_components],
            rx.icon(tag="pencil", id="icon"),
            rx.debounce_input(
                rx.input(on_change=lambda e: rx.redirect(e)), id="debounce-input"
            ),
        )


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

    # # get a reference to the connected client
    # token_input = driver.find_element(By.ID, "token")
    # assert token_input

    time.sleep(10)
    assert False
