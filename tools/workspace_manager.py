"""
💼 Workspace Manager - Standalone Version
Manages financial workspace, file organization, and data persistence
Handles workspace creation, backup, and maintenance
"""

import json
import os
import shutil
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

# Import standalone base tool
from tools.base_tool import BaseTool


class WorkspaceManager(BaseTool):
    """
    Workspace Manager - Financial workspace management

    Features:
    - Workspace creation and management
    - File organization and structure
    - Data backup and restoration
    - Workspace statistics
    - Data export capabilities
    """

    def __init__(self, workspace_path: str = None):
        """Initialize workspace manager"""
        super().__init__()

        if workspace_path:
            self.workspace_path = Path(workspace_path)
        else:
            # Default to user's home directory
            home_dir = Path.home()
            self.workspace_path = home_dir / "financial_workspace"

        # Ensure workspace exists
        self.workspace_path.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        self._create_directory_structure()

    def _create_directory_structure(self):
        """Create the standard workspace directory structure"""
        directories = [
            "transactions",
            "reports",
            "exports",
            "backups",
            "temp",
            "config"
        ]

        for directory in directories:
            dir_path = self.workspace_path / directory
            dir_path.mkdir(exist_ok=True)

        # Create .gitkeep files to preserve empty directories
        for directory in directories:
            gitkeep_path = self.workspace_path / directory / ".gitkeep"
            if not gitkeep_path.exists():
                gitkeep_path.touch()

    def ensure_workspace_exists(self) -> Path:
        """Ensure workspace exists and return path"""
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        self._create_directory_structure()

        # Create workspace info file if it doesn't exist
        info_file = self.workspace_path / "workspace_info.json"
        if not info_file.exists():
            self._create_workspace_info(info_file)

        return self.workspace_path

    def _create_workspace_info(self, info_file: Path):
        """Create workspace information file"""
        info = {
            "created_at": datetime.now().isoformat(),
            "created_by": "Personal In and Out Dashboard",
            "version": "1.0.0",
            "workspace_path": str(self.workspace_path),
            "last_backup": None,
            "total_backups": 0
        }

        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)

    def get_workspace_info(self) -> Dict[str, Any]:
        """Get comprehensive workspace information"""
        info_file = self.workspace_path / "workspace_info.json"

        if info_file.exists():
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
            except Exception:
                info = {}
        else:
            info = {}

        # Get current statistics
        stats = self.get_workspace_statistics()

        return {
            "path": str(self.workspace_path),
            "created_at": info.get("created_at"),
            "created_by": info.get("created_by", "Personal In and Out Dashboard"),
            "version": info.get("version", "1.0.0"),
            "last_backup": info.get("last_backup"),
            "total_backups": info.get("total_backups", 0),
            **stats
        }

    def get_workspace_statistics(self) -> Dict[str, Any]:
        """Get workspace file and data statistics"""
        stats = {
            "transaction_count": 0,
            "category_count": 0,
            "budget_count": 0,
            "report_count": 0,
            "backup_count": 0,
            "total_size_mb": 0,
            "last_modified": None
        }

        try:
            # Count files in each directory
            transactions_dir = self.workspace_path / "transactions"
            stats["transaction_count"] = len([
                f for f in transactions_dir.glob("*.json")
                if f.is_file()
            ])

            reports_dir = self.workspace_path / "reports"
            stats["report_count"] = len([
                f for f in reports_dir.glob("*")
                if f.is_file() and not f.name.startswith(".")
            ])

            backups_dir = self.workspace_path / "backups"
            stats["backup_count"] = len([
                f for f in backups_dir.glob("*")
                if f.is_file() and not f.name.startswith(".")
            ])

            # Count categories and budgets from config files
            master_db = self.workspace_path / "master_transaction_db.json"
            if master_db.exists():
                try:
                    with open(master_db, 'r') as f:
                        data = json.load(f)
                        stats["category_count"] = len(data.get("categories", {}))
                except Exception:
                    pass

            budgets_file = self.workspace_path / "budgets.json"
            if budgets_file.exists():
                try:
                    with open(budgets_file, 'r') as f:
                        budgets = json.load(f)
                        stats["budget_count"] = len(budgets)
                except Exception:
                    pass

            # Calculate total size
            total_size = 0
            last_modified = None

            for file_path in self.workspace_path.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if last_modified is None or file_mtime > last_modified:
                        last_modified = file_mtime

            stats["total_size_mb"] = round(total_size / (1024 * 1024), 2)
            stats["last_modified"] = last_modified.isoformat() if last_modified else None

        except Exception as e:
            print(f"Warning: Could not calculate workspace statistics: {e}")

        return stats

    def create_backup(self, include_reports: bool = True) -> Optional[str]:
        """Create a backup of the workspace"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"financial_backup_{timestamp}"
            backup_path = self.workspace_path / "backups" / f"{backup_name}.zip"

            # Create temporary backup directory
            temp_backup_path = self.workspace_path / "temp" / backup_name
            temp_backup_path.mkdir(parents=True, exist_ok=True)

            # Copy essential files and directories
            essential_items = [
                "master_transaction_db.json",
                "transactions",
                "currencies_config.json",
                "budgets.json"
            ]

            if include_reports:
                essential_items.append("reports")

            # Backup each item
            for item in essential_items:
                source_path = self.workspace_path / item
                if source_path.exists():
                    if source_path.is_file():
                        shutil.copy2(source_path, temp_backup_path)
                    elif source_path.is_dir():
                        shutil.copytree(source_path, temp_backup_path / item,
                                       ignore=shutil.ignore_patterns("*.tmp", ".gitkeep"))

            # Create backup info
            backup_info = {
                "created_at": datetime.now().isoformat(),
                "created_by": "Personal In and Out Dashboard",
                "backup_type": "manual",
                "includes_reports": include_reports,
                "workspace_path": str(self.workspace_path),
                "backup_version": "1.0"
            }

            with open(temp_backup_path / "backup_info.json", 'w') as f:
                json.dump(backup_info, f, indent=2)

            # Create zip file
            shutil.make_archive(str(backup_path.with_suffix('')), 'zip',
                              temp_backup_path.parent, backup_name)

            # Clean up temporary directory
            shutil.rmtree(temp_backup_path)

            # Update workspace info
            self._update_backup_info()

            backup_file = str(backup_path)
            print(f"✅ Backup created: {backup_file}")
            return backup_file

        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return None

    def _update_backup_info(self):
        """Update backup information in workspace"""
        info_file = self.workspace_path / "workspace_info.json"
        backup_count = len([
            f for f in (self.workspace_path / "backups").glob("*.zip")
            if f.is_file()
        ])

        info = {
            "last_backup": datetime.now().isoformat(),
            "total_backups": backup_count
        }

        # Update existing info or create new
        if info_file.exists():
            try:
                with open(info_file, 'r') as f:
                    existing_info = json.load(f)
                existing_info.update(info)
                info = existing_info
            except Exception:
                pass

        with open(info_file, 'w') as f:
            json.dump(info, f, indent=2)

    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups"""
        backups = []
        backups_dir = self.workspace_path / "backups"

        for backup_file in backups_dir.glob("*.zip"):
            if backup_file.is_file():
                # Extract info from backup filename and file stats
                stat = backup_file.stat()
                backup_info = {
                    "filename": backup_file.name,
                    "path": str(backup_file),
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
                }

                # Try to read backup info from the zip if possible
                try:
                    import zipfile
                    with zipfile.ZipFile(backup_file, 'r') as zip_file:
                        if "backup_info.json" in zip_file.namelist():
                            with zip_file.open("backup_info.json") as info_file:
                                backup_data = json.load(info_file.read().decode('utf-8'))
                                backup_info.update(backup_data)
                except Exception:
                    pass

                backups.append(backup_info)

        # Sort by creation date (newest first)
        backups.sort(key=lambda x: x["created_at"], reverse=True)
        return backups

    def restore_backup(self, backup_path: str, force: bool = False) -> bool:
        """Restore workspace from backup"""
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                print(f"❌ Backup file not found: {backup_path}")
                return False

            if not force:
                # Ask for confirmation
                response = input(f"⚠️ This will overwrite current workspace. Continue? (y/N): ")
                if response.lower() not in ['y', 'yes']:
                    print("Backup restoration cancelled.")
                    return False

            # Create temp directory for extraction
            temp_extract_path = self.workspace_path / "temp" / f"restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            temp_extract_path.mkdir(parents=True, exist_ok=True)

            # Extract backup
            import zipfile
            with zipfile.ZipFile(backup_file, 'r') as zip_file:
                zip_file.extractall(temp_extract_path)

            # Restore files
            backup_items = [
                "master_transaction_db.json",
                "transactions",
                "currencies_config.json",
                "budgets.json",
                "reports"
            ]

            for item in backup_items:
                source_path = temp_extract_path / item
                if source_path.exists():
                    target_path = self.workspace_path / item

                    # Remove existing target if it exists
                    if target_path.exists():
                        if target_path.is_file():
                            target_path.unlink()
                        elif target_path.is_dir():
                            shutil.rmtree(target_path)

                    # Copy restored item
                    if source_path.is_file():
                        shutil.copy2(source_path, target_path)
                    elif source_path.is_dir():
                        shutil.copytree(source_path, target_path)

            # Clean up
            shutil.rmtree(temp_extract_path)

            print(f"✅ Workspace restored from backup: {backup_path}")
            return True

        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return False

    def clean_workspace(self, dry_run: bool = True) -> Dict[str, Any]:
        """Clean up temporary and old files"""
        results = {
            "files_removed": [],
            "space_freed_mb": 0,
            "errors": []
        }

        try:
            # Clean temp directory
            temp_dir = self.workspace_path / "temp"
            if temp_dir.exists():
                for item in temp_dir.iterdir():
                    try:
                        if item.is_file():
                            size_mb = round(item.stat().st_size / (1024 * 1024), 2)
                            if not dry_run:
                                item.unlink()
                            results["files_removed"].append(str(item))
                            results["space_freed_mb"] += size_mb
                        elif item.is_dir() and item.name not in [".gitkeep"]:
                            size_mb = sum(
                                f.stat().st_size for f in item.rglob("*") if f.is_file()
                            ) / (1024 * 1024)
                            if not dry_run:
                                shutil.rmtree(item)
                            results["files_removed"].append(str(item))
                            results["space_freed_mb"] += round(size_mb, 2)
                    except Exception as e:
                        results["errors"].append(f"Error removing {item}: {e}")

            # Clean old backups (keep last 10)
            backups = self.list_backups()
            old_backups = backups[10:]  # Keep only the 10 most recent

            for backup in old_backups:
                try:
                    backup_path = Path(backup["path"])
                    size_mb = backup["size_mb"]
                    if not dry_run:
                        backup_path.unlink()
                    results["files_removed"].append(backup["path"])
                    results["space_freed_mb"] += size_mb
                except Exception as e:
                    results["errors"].append(f"Error removing backup {backup['filename']}: {e}")

            if dry_run:
                print("🔍 Dry run - no files were actually removed")
            else:
                print("✅ Workspace cleaned successfully")

        except Exception as e:
            results["errors"].append(f"General cleaning error: {e}")

        return results

    def export_data(self, export_path: str = None, include_transactions: bool = True,
                   include_categories: bool = True, include_budgets: bool = True) -> Optional[str]:
        """Export workspace data to a specified location"""
        try:
            if export_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                export_path = self.workspace_path / "exports" / f"financial_export_{timestamp}.json"

            export_path = Path(export_path)
            export_path.parent.mkdir(parents=True, exist_ok=True)

            export_data = {
                "export_info": {
                    "created_at": datetime.now().isoformat(),
                    "created_by": "Personal In and Out Dashboard",
                    "workspace_path": str(self.workspace_path),
                    "export_version": "1.0"
                }
            }

            # Export categories
            if include_categories:
                categories_file = self.workspace_path / "master_transaction_db.json"
                if categories_file.exists():
                    with open(categories_file, 'r') as f:
                        categories_data = json.load(f)
                        export_data["categories"] = categories_data

            # Export transactions
            if include_transactions:
                transactions_dir = self.workspace_path / "transactions"
                transactions = []
                for transaction_file in transactions_dir.glob("*.json"):
                    try:
                        with open(transaction_file, 'r') as f:
                            transaction_data = json.load(f)
                            transactions.append(transaction_data)
                    except Exception:
                        continue
                export_data["transactions"] = transactions

            # Export budgets
            if include_budgets:
                budgets_file = self.workspace_path / "budgets.json"
                if budgets_file.exists():
                    with open(budgets_file, 'r') as f:
                        budgets_data = json.load(f)
                        export_data["budgets"] = budgets_data

            # Export currencies
            currencies_file = self.workspace_path / "currencies_config.json"
            if currencies_file.exists():
                with open(currencies_file, 'r') as f:
                    currencies_data = json.load(f)
                    export_data["currencies"] = currencies_data

            # Save export file
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            export_str = str(export_path)
            print(f"✅ Data exported to: {export_str}")
            return export_str

        except Exception as e:
            print(f"❌ Error exporting data: {e}")
            return None

    def _execute(self, **kwargs) -> str:
        """Execute tool operation (required by BaseTool)"""
        operation = kwargs.get("operation", "info")

        try:
            if operation == "info":
                info = self.get_workspace_info()
                return f"Workspace Info: {json.dumps(info, indent=2)}"
            elif operation == "statistics":
                stats = self.get_workspace_statistics()
                return f"Workspace Statistics: {json.dumps(stats, indent=2)}"
            elif operation == "create_backup":
                backup_path = self.create_backup()
                if backup_path:
                    return f"✅ Backup created: {backup_path}"
                else:
                    return "❌ Backup creation failed"
            elif operation == "list_backups":
                backups = self.list_backups()
                return f"Available Backups: {json.dumps(backups, indent=2)}"
            else:
                return f"Unknown operation: {operation}"

        except Exception as e:
            return f"❌ Error: {str(e)}"


if __name__ == "__main__":
    # Example usage
    manager = WorkspaceManager()
    workspace_path = manager.ensure_workspace_exists()

    print("=== Personal In and Out Dashboard - Workspace Manager ===")
    print(f"Workspace path: {workspace_path}")

    info = manager.get_workspace_info()
    print(f"Created: {info.get('created_at')}")
    print(f"Reports: {info.get('report_count', 0)}")
    print(f"Backups: {info.get('total_backups', 0)}")
    print(f"Size: {info.get('total_size_mb', 0)} MB")

    # Create a backup
    print(f"\n💾 Creating backup...")
    backup_path = manager.create_backup()
    if backup_path:
        print(f"Backup created: {backup_path}")