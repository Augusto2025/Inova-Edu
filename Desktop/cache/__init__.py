"""
Sistema de Cache Inteligente para Desktop
Cache em memória com TTL e invalidação automática por tags
"""
import time
import threading
from typing import Any, Optional, Callable, List, Dict
from dataclasses import dataclass, field
from functools import wraps


@dataclass
class CacheEntry:
    """Entrada do cache com metadados"""
    value: Any
    expires_at: float
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


class CacheManager:
    """
    Gerenciador de cache thread-safe com suporte a:
    - TTL (Time To Live)
    - Tags para invalidação em lote
    - Callbacks de invalidação
    """

    def __init__(self, default_ttl: int = 300):  # 5 min default
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self._default_ttl = default_ttl
        self._callbacks: Dict[str, List[Callable]] = {}

    def _is_expired(self, entry: CacheEntry) -> bool:
        return time.time() > entry.expires_at

    def _cleanup_expired(self):
        """Remove entradas expiradas"""
        now = time.time()
        with self._lock:
            expired_keys = [k for k, v in self._cache.items() if now > v.expires_at]
            for k in expired_keys:
                del self._cache[k]

    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache se não expirado"""
        self._cleanup_expired()
        with self._lock:
            entry = self._cache.get(key)
            if entry and not self._is_expired(entry):
                return entry.value
            elif entry:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: int = None, tags: List[str] = None) -> None:
        """Armazena valor no cache com TTL e tags"""
        ttl = ttl or self._default_ttl
        tags = tags or []
        expires_at = time.time() + ttl

        with self._lock:
            self._cache[key] = CacheEntry(
                value=value,
                expires_at=expires_at,
                tags=tags
            )

            # Indexa por tag para invalidação rápida
            for tag in tags:
                if tag not in self._callbacks:
                    self._callbacks[tag] = []

    def delete(self, key: str) -> bool:
        """Remove uma chave específica do cache"""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                # Remove das tags
                for tag in entry.tags:
                    if tag in self._callbacks:
                        self._callbacks[tag] = [k for k in self._callbacks[tag] if k != key]
                del self._cache[key]
                return True
        return False

    def invalidate_tag(self, tag: str) -> int:
        """Invalida todas as entradas com uma tag específica"""
        count = 0
        with self._lock:
            keys_to_delete = [
                k for k, v in self._cache.items()
                if tag in v.tags
            ]
            for key in keys_to_delete:
                del self._cache[key]
                count += 1

            # Executa callbacks de invalidação
            for callback in self._callbacks.get(tag, []):
                try:
                    callback()
                except Exception:
                    pass
        return count

    def invalidate_keys(self, keys: List[str]) -> int:
        """Invalida múltiplas chaves de uma vez"""
        count = 0
        with self._lock:
            for key in keys:
                if key in self._cache:
                    del self._cache[key]
                    count += 1
        return count

    def clear(self) -> int:
        """Limpa todo o cache"""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            self._callbacks.clear()
        return count

    def register_invalidation_callback(self, tag: str, callback: Callable):
        """Registra callback para ser chamado quando tag for invalidada"""
        with self._lock:
            if tag not in self._callbacks:
                self._callbacks[tag] = []
            self._callbacks[tag].append(callback)

    def get_stats(self) -> Dict:
        """Retorna estatísticas do cache"""
        self._cleanup_expired()
        with self._lock:
            return {
                "total_entries": len(self._cache),
                "tags": list(self._callbacks.keys()),
                "memory_approx_kb": sum(
                    len(str(v.value)) for v in self._cache.values()
                ) / 1024
            }


# Instância global do cache
cache = CacheManager(default_ttl=300)  # 5 minutos default


# Decorators para uso fácil em métodos de modelo
def cached(ttl: int = 300, tags: List[str] = None, key_prefix: str = "", skip_self: bool = True):
    """
    Decorator para cachear resultado de método.

    Args:
        ttl: Tempo de vida em segundos
        tags: Tags para invalidação em grupo
        key_prefix: Prefixo para a chave do cache
        skip_self: Se True, pula o primeiro argumento (self) para métodos de instância
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Gera chave baseada no nome da função e argumentos
            key_parts = [key_prefix, func.__name__]
            start_idx = 1 if (skip_self and args) else 0
            key_parts.extend(str(a) for a in args[start_idx:])
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)

            # Tenta buscar do cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Executa função e cacheia resultado
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl, tags=tags or [])
            return result
        return wrapper
    return decorator


def invalidate_on_write(tags: List[str] = None, keys: List[str] = None):
    """
    Decorator para invalidar cache após escrita (INSERT/UPDATE/DELETE).

    Args:
        tags: Tags para invalidar
        keys: Chaves específicas para invalidar
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Invalida cache após escrita bem-sucedida
            if tags:
                for tag in tags:
                    cache.invalidate_tag(tag)
            if keys:
                cache.invalidate_keys(keys)
            return result
        return wrapper
    return decorator


# Helpers para tags comuns
class CacheTags:
    """Tags padrão para invalidação coordenada"""
    USUARIO = "usuario"
    PROJETO = "projeto"
    PASTA = "pasta"
    ARQUIVO = "arquivo"
    EVENTO = "evento"
    TURMA = "turma"
    CURSO = "curso"
    FORUM = "forum"
    PERFIL = "perfil"
    REPOSITORIO = "repositorio"

    @staticmethod
    def usuario_especifico(user_id: int) -> str:
        return f"usuario:{user_id}"

    @staticmethod
    def projeto_especifico(projeto_id: int) -> str:
        return f"projeto:{projeto_id}"

    @staticmethod
    def turma_especifica(turma_id: int) -> str:
        return f"turma:{turma_id}"