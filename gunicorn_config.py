import multiprocessing

bind = "0.0.0.0:8000"

# Otimização para Hetzner CPX11 (2 vCPU / 2GB RAM)
# Workers = (2 x CPU) + 1 = 5. Mas usamos 3 para economizar RAM.
workers = 3
# Threads ajudam quando o banco de dados demora a responder
threads = 4
worker_class = "gthread"

# Configurações de segurança e timeout
timeout = 60
keepalive = 5
accesslog = "-"
errorlog = "-"