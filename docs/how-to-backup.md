# How to backup database


1. Install sqlite on server:
    
    ```
    sudo apt update
    sudo apt install sqlite3
    ```

2. Create crontab entry
    
    ```bash
    crontab -e
    ```

    Place inside command like this.
    ```bash
    0 2 * * * sqlite3 /var/www/finman/data/*.db ".backup '/root/database/finman-$(date +\%Y\%m\%d\%H\%M\%S).db'"
    ```
    It assumes you have your database in `/var/www/finman/data/*.db` directory.
    
    It will create a safe copy of the database to the `/root/database/` directory, every day at 2 am.

3. Download database
    
    To properly backup you data you need to export the database from your server to another machine.

    I recommend to use `rsync` for that.

    Example command:

    ```bash
    rsync -azrvh --progress -e "ssh -p $PORT" --exclude={'.venv','.git','node_modules','.ruff*','__pycache__'} $HOST:/root/database/ $HOME/database/
    ```