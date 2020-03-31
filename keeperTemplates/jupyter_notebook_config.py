from SeafileContentManager import SeafileContentManager, SeafileCheckpoints
c = get_config()
c.NotebookApp.contents_manager_class = SeafileContentManager
c.ContentsManager.checkpoints_class = SeafileCheckpoints
