"""
Graphics and Visualization Module
Provides enhanced ASCII art and visual representations for the game
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.progress import BarColumn, Progress, TextColumn
import os


console = Console()


# ASCII Art Maps for different terrains
TERRAIN_MAPS = {
    'river_valley': """
     ~~~  ~~~  ~~~  ~~~  ~~~
    ~~~ [🏛️]  ~~~  ~~~  ~~~
     ~~~  ~~~  ~~~  ~~~  ~~~
    """,
    'coastal': """
     ≈≈≈ ≈≈≈ ≈≈≈ ≈≈≈ ≈≈≈
    ≈≈≈[🏛️]🏖️ ≈≈≈ ≈≈≈
     ≈≈≈ ≈≈≈ ≈≈≈ ≈≈≈ ≈≈≈
    """,
    'plains': """
     ╔═══╦═══╦═══╦═══╗
     ║ . ║[🏛️]║ . ║ . ║
     ╠═══╬═══╬═══╬═══╣
     ║ . ║ . ║ . ║ . ║
     ╚═══╩═══╩═══╩═══╝
    """,
    'forest': """
     🌲 🌲 🌲 🌲 🌲
    🌲🌲[🏛️]🌲🌲
     🌲 🌲 🌲 🌲 🌲
    """,
    'hills': """
     △ △ △ △ △
    △△△[🏛️]△△
     △ △ △ △ △
    """,
    'mountains': """
     ⛰️  ⛰️  ⛰️  ⛰️
    ⛰️[🏛️]⛰️
     ⛰️  ⛰️  ⛰️  ⛰️
    """,
    'desert': """
     ░░░ ░░░ ░░░ ░░░
    ░░░[🏛️]░░░
     ░░░ ░░░ ░░░ ░░░
    """
}

# Technology era colors
ERA_COLORS = {
    'early_neolithic': 'bright_yellow',
    'middle_neolithic': 'yellow',
    'late_neolithic': 'bright_cyan',
    'chalcolithic': 'magenta'
}


def draw_header(title: str, subtitle: str = "", width: int = 60):
    """Draw a fancy header"""
    console.print()
    console.rule(f"[bold cyan]{title}[/bold cyan]", style="cyan")
    if subtitle:
        console.print(Align.center(f"[dim]{subtitle}[/dim]"), width=width)
    console.print()


def draw_game_title():
    """Draw the main game title with ASCII art"""
    title = """
    [bold cyan]╔════════════════════════════════════════════╗[/bold cyan]
    [bold cyan]║[/bold cyan]  [bold yellow]ANCESTRAL HABITATION[/bold yellow]  [bold cyan]║[/bold cyan]
    [bold cyan]║[/bold cyan]  [bold green]~ A Neolithic Era Strategy Game ~[/bold green]  [bold cyan]║[/bold cyan]
    [bold cyan]║[/bold cyan]        [bold cyan](8000 BC - 1200 BC)[/bold cyan]       [bold cyan]║[/bold cyan]
    [bold cyan]╚════════════════════════════════════════════╝[/bold cyan]
    """
    console.print(title)


def draw_terrain_map(geography_type: str):
    """Display a simple ASCII map of the current terrain"""
    map_art = TERRAIN_MAPS.get(geography_type, TERRAIN_MAPS['plains'])
    panel = Panel(map_art, title="[bold cyan]Territory Map[/bold cyan]", 
                  border_style="cyan", expand=False)
    console.print(panel)


def draw_resource_bars(resources: dict, width: int = 40):
    """Draw visual bars for resources"""
    colors = {
        'food': 'yellow',
        'wood': '#8B4513',
        'stone': 'white',
        'clay': '#D2B48C',
        'hides': '#8B7355',
    }
    
    console.print("[bold cyan]Resources:[/bold cyan]")
    for resource, amount in sorted(resources.items()):
        color = colors.get(resource, 'white')
        # Create a simple bar
        bar_length = min(int(amount / 50), 30)  # Cap at 30 chars
        bar = "█" * bar_length + "░" * (30 - bar_length)
        resource_text = f"  {resource.capitalize():<10} [{bar}] {amount:>5}"
        console.print(resource_text, style=color)


def draw_population_status(population: int, max_population: int = 10000):
    """Draw population status with a progress bar"""
    progress = Progress(
        TextColumn("[cyan]{task.description}"),
        BarColumn(),
        TextColumn("[bold cyan]{task.percentage:>3.0f}%"),
    )
    
    with progress:
        task = progress.add_task(f"Population: {population}", total=max_population)
        progress.update(task, completed=min(population, max_population))


def draw_status_panel(game_state):
    """Draw a comprehensive status panel"""
    from game_engine.geography import GEOGRAPHIES, get_current_season
    from game_engine.governance import GOVERNANCE_TYPES
    
    # Year display
    year_bc_ad = f"{abs(game_state.year)} BC" if game_state.year < 0 else f"{game_state.year} AD"
    
    # Get current season
    season = get_current_season(game_state.turn)
    
    # Geography info
    geo = GEOGRAPHIES[game_state.geography_type]
    
    # Governance info
    gov = GOVERNANCE_TYPES[game_state.governance_type]
    
    # Build status text
    status_text = f"""
[bold cyan]Year:[/bold cyan] {year_bc_ad} (Turn {game_state.turn})
[bold cyan]Tribe:[/bold cyan] {game_state.tribe_name}
[bold cyan]Season:[/bold cyan] {season.name}

[bold yellow]Population:[/bold yellow] {game_state.population}
[bold yellow]Governance:[/bold yellow] {gov.display_name} (Stability: {game_state.governance_stability}%)
[bold yellow]Location:[/bold yellow] {geo.name}

[bold green]Technologies:[/bold green] {len(game_state.technologies)} discovered
[bold green]Culture Points:[/bold green] {game_state.culture_points}
[bold green]Farms:[/bold green] {game_state.farms} (Level {game_state.farming_level})
"""
    
    if game_state.has_writing:
        status_text += "[bold magenta]✓ Writing System Developed[/bold magenta]\n"
    
    panel = Panel(status_text, title="[bold cyan]Civilization Status[/bold cyan]", 
                  border_style="cyan")
    console.print(panel)


def draw_technology_tree(technologies_dict: dict, discovered: set):
    """Draw an organized technology tree display"""
    table = Table(title="[bold cyan]Technology Tree[/bold cyan]", show_header=True,
                  header_style="bold cyan", border_style="cyan")
    
    table.add_column("Technology", style="dim", width=20)
    table.add_column("Era", style="dim", width=15)
    table.add_column("Status", width=10)
    
    # Organize by era
    by_era = {}
    for tech_name, tech in technologies_dict.items():
        era = tech.era
        if era not in by_era:
            by_era[era] = []
        by_era[era].append((tech_name, tech))
    
    # Display by era
    for era in sorted(by_era.keys()):
        techs = by_era[era]
        era_color = ERA_COLORS.get(era, 'white')
        
        for tech_name, tech in sorted(techs):
            status = "✓ Discovered" if tech_name in discovered else "Available"
            status_color = "green" if tech_name in discovered else "yellow"
            
            table.add_row(
                tech.name,
                f"[{era_color}]{era.replace('_', ' ').title()}[/{era_color}]",
                f"[{status_color}]{status}[/{status_color}]"
            )
    
    console.print(table)


def draw_action_menu():
    """Draw a styled action menu"""
    console.rule("[bold cyan]Available Actions[/bold cyan]", style="cyan")
    actions = [
        "[bold cyan]1.[/bold cyan] Advance to next year",
        "[bold yellow]2.[/bold yellow] Build farm",
        "[bold green]3.[/bold green] Research technology",
        "[bold magenta]4.[/bold magenta] Migrate to new location",
        "[bold white]5.[/bold white] Change governance",
        "[bold cyan]6.[/bold cyan] View technologies",
        "[bold cyan]7.[/bold cyan] View available locations",
        "[bold cyan]8.[/bold cyan] View statistics",
        "[bold red]9.[/bold red] Quit game",
    ]
    
    for action in actions:
        console.print(f"  {action}")
    
    console.rule(style="cyan")


def draw_location_details(geography_type: str, geographies_dict: dict):
    """Draw detailed location information"""
    geo = geographies_dict.get(geography_type)
    if not geo:
        return
    
    details = f"""
[bold cyan]Location:[/bold cyan] {geo.name}
[bold cyan]Climate:[/bold cyan] {geo.climate}
[bold cyan]Description:[/bold cyan]
  {geo.description}

[bold cyan]Resource Modifiers:[/bold cyan]
"""
    
    for resource, modifier in geo.resource_modifiers.items():
        modifier_color = "green" if modifier > 1.0 else "red" if modifier < 1.0 else "white"
        details += f"  {resource.capitalize()}: [{modifier_color}]{modifier:.1f}x[/{modifier_color}]\n"
    
    details += f"\n[bold cyan]Migration Difficulty:[/bold cyan] {geo.migration_difficulty}/10"
    
    panel = Panel(details, title="[bold cyan]Location Details[/bold cyan]", 
                  border_style="cyan")
    console.print(panel)


def draw_statistics(game_state):
    """Draw comprehensive game statistics"""
    from game_engine.geography import GEOGRAPHIES
    from game_engine.governance import GOVERNANCE_TYPES
    
    geo = GEOGRAPHIES[game_state.geography_type]
    gov = GOVERNANCE_TYPES[game_state.governance_type]
    
    # Create a statistics table
    table = Table(title="[bold green]Game Statistics[/bold green]", 
                  show_header=False, border_style="green")
    
    table.add_row("[bold cyan]Tribe Name[/bold cyan]", game_state.tribe_name)
    
    year_display = f"{abs(game_state.year)} BC" if game_state.year < 0 else f"{game_state.year} AD"
    table.add_row("[bold cyan]Current Year[/bold cyan]", year_display)
    table.add_row("[bold cyan]Total Turns[/bold cyan]", str(game_state.turn))
    
    table.add_row("[bold yellow]Population[/bold yellow]", str(game_state.population))
    table.add_row("[bold yellow]Governance Type[/bold yellow]", gov.display_name)
    table.add_row("[bold yellow]Governance Stability[/bold yellow]", 
                  f"{game_state.governance_stability}%")
    
    table.add_row("[bold green]Current Location[/bold green]", geo.name)
    table.add_row("[bold green]Farms[/bold green]", 
                  f"{game_state.farms} (Level {game_state.farming_level})")
    table.add_row("[bold green]Culture Points[/bold green]", str(game_state.culture_points))
    
    table.add_row("[bold magenta]Technologies Discovered[/bold magenta]", 
                  str(len(game_state.technologies)))
    table.add_row("[bold magenta]Writing System[/bold magenta]", 
                  "✓ Yes" if game_state.has_writing else "✗ No")
    
    console.print(table)


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def draw_event_notification(event_title: str, event_description: str):
    """Draw a styled event notification"""
    panel = Panel(
        f"[bold]{event_description}[/bold]",
        title=f"[bold yellow]⚠ {event_title}[/bold yellow]",
        border_style="yellow",
        expand=False
    )
    console.print(panel)


def draw_success_message(message: str):
    """Draw a success message"""
    console.print(f"[bold green]✓ {message}[/bold green]")


def draw_error_message(message: str):
    """Draw an error message"""
    console.print(f"[bold red]✗ {message}[/bold red]")


def draw_info_message(message: str):
    """Draw an info message"""
    console.print(f"[bold cyan]ℹ {message}[/bold cyan]")
