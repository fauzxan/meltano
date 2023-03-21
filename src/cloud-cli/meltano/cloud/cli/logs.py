"""Meltano Cloud `logs` command."""

from __future__ import annotations

import asyncio
import sys
import typing as t

import click

from meltano.cloud.api.client import MeltanoCloudClient
from meltano.cloud.cli.base import cloud

if t.TYPE_CHECKING:
    from meltano.cloud.api.config import MeltanoCloudConfig


@cloud.group()
def logs() -> None:
    """Meltano Cloud `logs` command."""


async def print_logs(
    config: MeltanoCloudConfig,
    execution_id: str,
) -> None:
    """Print the logs.

    Args:
        execution_id: The execution identifier.
        config: the meltano config to use
    """
    async with MeltanoCloudClient(config=config) as client:
        async with client.stream_logs(execution_id) as response:
            async for chunk in response.content.iter_any():
                sys.stdout.buffer.write(chunk)
                sys.stdout.flush()


@logs.command("print")
@click.option("--execution-id", required=True)
@click.pass_context
def print_(context: click.Context, execution_id: str) -> None:
    """Print the logs.

    Args:
        context: The Click context.
        execution_id: The execution identifier.
    """
    config: MeltanoCloudConfig = context.obj["config"]

    click.echo(f"Fetching logs for execution {execution_id}")

    asyncio.run(print_logs(config, execution_id))