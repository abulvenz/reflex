"""Stub file for reflex/components/base/error_boundary.py"""

# ------------------- DO NOT EDIT ----------------------
# This file was generated by `reflex/utils/pyi_generator.py`!
# ------------------------------------------------------
from typing import Any, Callable, Dict, List, Optional, Union, overload

from reflex.components.component import Component
from reflex.event import EventHandler, EventSpec
from reflex.ivars.base import ImmutableVar
from reflex.style import Style
from reflex.utils.imports import ImportVar
from reflex.vars import Var

class ErrorBoundary(Component):
    def add_imports(self) -> dict[str, list[ImportVar]]: ...
    def add_hooks(self) -> List[str | ImmutableVar]: ...
    def add_custom_code(self) -> List[str]: ...
    @overload
    @classmethod
    def create(  # type: ignore
        cls,
        *children,
        Fallback_component: Optional[Union[Var[Component], Component]] = None,
        style: Optional[Style] = None,
        key: Optional[Any] = None,
        id: Optional[Any] = None,
        class_name: Optional[Any] = None,
        autofocus: Optional[bool] = None,
        custom_attrs: Optional[Dict[str, Union[ImmutableVar, str]]] = None,
        on_blur: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_click: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_context_menu: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_double_click: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_error: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_focus: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_mount: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_mouse_down: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_mouse_enter: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_mouse_leave: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_mouse_move: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_mouse_out: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_mouse_over: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_mouse_up: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_scroll: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        on_unmount: Optional[
            Union[EventHandler, EventSpec, list, Callable, ImmutableVar]
        ] = None,
        **props,
    ) -> "ErrorBoundary":
        """Create the component.

        Args:
            *children: The children of the component.
            Fallback_component: Rendered instead of the children when an error is caught.
            style: The style of the component.
            key: A unique key for the component.
            id: The id for the component.
            class_name: The class name for the component.
            autofocus: Whether the component should take the focus once the page is loaded
            custom_attrs: custom attribute
            **props: The props of the component.

        Returns:
            The component.
        """
        ...

error_boundary = ErrorBoundary.create
