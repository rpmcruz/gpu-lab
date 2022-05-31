import sqlite3, json

NGPUS = 4

def init():
    con = sqlite3.connect('processes.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE processes (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, cmd TEXT, nice INT, gpu INT, pid INT)')
    con.commit()
    con.close()

def add(user, cmd, nice, gpu, pid):
    con = sqlite3.connect('processes.db')
    cur = con.cursor()
    cur.execute('INSERT INTO processes (user, cmd, nice, gpu, pid) VALUES (?, ?, ?, ?, ?)', (user, json.dumps(cmd), nice, gpu, pid))
    con.commit()
    con.close()

def remove(id):
    con = sqlite3.connect('processes.db')
    cur = con.cursor()
    cur.execute('DELETE FROM processes WHERE id = ?', (id,))
    con.commit()
    con.close()

def assign_gpu_pid(id, gpu, pid):
    con = sqlite3.connect('processes.db')
    cur = con.cursor()
    cur.execute('UPDATE processes SET gpu = ?, pid = ? WHERE id = ?', (gpu, pid, id))
    con.commit()
    con.close()

def get_ids_cmds_queue():
    con = sqlite3.connect('processes.db')
    cur = con.cursor()
    l = list(cur.execute('SELECT id, cmd FROM processes WHERE gpu = -1'))
    con.close()
    return [(id, json.loads(cmd)) for id, cmd in l]

def get_ids_pids_gpus_cmds_running():
    con = sqlite3.connect('processes.db')
    cur = con.cursor()
    l = list(cur.execute('SELECT id, pid, gpu, cmd FROM processes WHERE gpu != -1'))
    con.close()
    return l

def get_pid(id):
    con = sqlite3.connect('processes.db')
    cur = con.cursor()
    cur.execute('SELECT id, pid FROM processes WHERE id != ?', (id,))
    ret = cur.fetchone()
    con.close()
    return ret

def get_gpus_available():
    con = sqlite3.connect('processes.db')
    cur = con.cursor()
    used_gpus = set(i[0] for i in cur.execute('SELECT gpu FROM processes WHERE gpu != -1'))
    gpus = set(range(NGPUS)) - used_gpus
    con.close()
    return gpus

def get_meanest():
    con = sqlite3.connect('processes.db')
    cur = con.cursor()
    cur.execute('SELECT id FROM processes WHERE gpu = -1 ORDER BY nice ASC LIMIT 1')
    id = cur.fetchone()
    con.close()
    return id
