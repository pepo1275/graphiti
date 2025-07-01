"""
Integration layer for token monitoring in Graphiti
Hooks into LLM and embedding clients to track usage automatically
"""

from typing import Dict, Any, Optional, Callable
from functools import wraps
import asyncio
from graphiti_core.telemetry.token_monitor import get_token_monitor, ServiceType

def track_llm_usage(provider: str, model: str, operation: str = "inference"):
    """Decorator to track LLM token usage."""
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            monitor = get_token_monitor()
            api_key = kwargs.get('api_key') or getattr(args[0], 'api_key', None) if args else None
            
            try:
                result = await func(*args, **kwargs)
                
                # Extract token counts from result
                usage_info = _extract_token_info(result, provider)
                if usage_info:
                    monitor.log_usage(
                        provider=provider,
                        service_type=ServiceType.LLM,
                        model=model,
                        operation=operation,
                        input_tokens=usage_info.get('input_tokens', 0),
                        output_tokens=usage_info.get('output_tokens', 0),
                        api_key=api_key,
                        metadata={
                            'function': func.__name__,
                            'success': True
                        }
                    )
                
                return result
                
            except Exception as e:
                # Log error
                monitor.log_usage(
                    provider=provider,
                    service_type=ServiceType.LLM,
                    model=model,
                    operation=operation,
                    input_tokens=0,
                    output_tokens=0,
                    api_key=api_key,
                    error=True,
                    error_message=str(e),
                    metadata={'function': func.__name__}
                )
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            monitor = get_token_monitor()
            api_key = kwargs.get('api_key') or getattr(args[0], 'api_key', None) if args else None
            
            try:
                result = func(*args, **kwargs)
                
                # Extract token counts from result
                usage_info = _extract_token_info(result, provider)
                if usage_info:
                    monitor.log_usage(
                        provider=provider,
                        service_type=ServiceType.LLM,
                        model=model,
                        operation=operation,
                        input_tokens=usage_info.get('input_tokens', 0),
                        output_tokens=usage_info.get('output_tokens', 0),
                        api_key=api_key,
                        metadata={
                            'function': func.__name__,
                            'success': True
                        }
                    )
                
                return result
                
            except Exception as e:
                # Log error
                monitor.log_usage(
                    provider=provider,
                    service_type=ServiceType.LLM,
                    model=model,
                    operation=operation,
                    input_tokens=0,
                    output_tokens=0,
                    api_key=api_key,
                    error=True,
                    error_message=str(e),
                    metadata={'function': func.__name__}
                )
                raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

def track_embedding_usage(provider: str, model: str, operation: str = "embed"):
    """Decorator to track embedding token usage."""
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            monitor = get_token_monitor()
            api_key = kwargs.get('api_key') or getattr(args[0], 'api_key', None) if args else None
            
            try:
                # Get input text for token counting
                input_text = _extract_embedding_input(args, kwargs)
                input_tokens = _estimate_tokens(input_text)
                
                result = await func(*args, **kwargs)
                
                monitor.log_usage(
                    provider=provider,
                    service_type=ServiceType.EMBEDDING,
                    model=model,
                    operation=operation,
                    input_tokens=input_tokens,
                    output_tokens=0,  # Embeddings don't have output tokens
                    api_key=api_key,
                    metadata={
                        'function': func.__name__,
                        'success': True,
                        'vector_dims': len(result[0]) if isinstance(result, list) and result else None
                    }
                )
                
                return result
                
            except Exception as e:
                monitor.log_usage(
                    provider=provider,
                    service_type=ServiceType.EMBEDDING,
                    model=model,
                    operation=operation,
                    input_tokens=0,
                    output_tokens=0,
                    api_key=api_key,
                    error=True,
                    error_message=str(e),
                    metadata={'function': func.__name__}
                )
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            monitor = get_token_monitor()
            api_key = kwargs.get('api_key') or getattr(args[0], 'api_key', None) if args else None
            
            try:
                # Get input text for token counting
                input_text = _extract_embedding_input(args, kwargs)
                input_tokens = _estimate_tokens(input_text)
                
                result = func(*args, **kwargs)
                
                monitor.log_usage(
                    provider=provider,
                    service_type=ServiceType.EMBEDDING,
                    model=model,
                    operation=operation,
                    input_tokens=input_tokens,
                    output_tokens=0,  # Embeddings don't have output tokens
                    api_key=api_key,
                    metadata={
                        'function': func.__name__,
                        'success': True,
                        'vector_dims': len(result[0]) if isinstance(result, list) and result else None
                    }
                )
                
                return result
                
            except Exception as e:
                monitor.log_usage(
                    provider=provider,
                    service_type=ServiceType.EMBEDDING,
                    model=model,
                    operation=operation,
                    input_tokens=0,
                    output_tokens=0,
                    api_key=api_key,
                    error=True,
                    error_message=str(e),
                    metadata={'function': func.__name__}
                )
                raise
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

def _extract_token_info(result: Any, provider: str) -> Optional[Dict[str, int]]:
    """Extract token usage information from API response."""
    if not result:
        return None
    
    # OpenAI format
    if provider == "openai" and hasattr(result, 'usage'):
        return {
            'input_tokens': result.usage.prompt_tokens,
            'output_tokens': result.usage.completion_tokens
        }
    
    # Anthropic format
    elif provider == "anthropic" and hasattr(result, 'usage'):
        return {
            'input_tokens': result.usage.input_tokens,
            'output_tokens': result.usage.output_tokens
        }
    
    # Gemini format
    elif provider == "gemini" and hasattr(result, 'usage_metadata'):
        return {
            'input_tokens': result.usage_metadata.prompt_token_count,
            'output_tokens': result.usage_metadata.candidates_token_count
        }
    
    return None

def _extract_embedding_input(args: tuple, kwargs: dict) -> str:
    """Extract input text from embedding function arguments."""
    # Common parameter names for text input
    for param in ['text', 'texts', 'input', 'inputs', 'content']:
        if param in kwargs:
            value = kwargs[param]
            if isinstance(value, list):
                return ' '.join(str(v) for v in value)
            return str(value)
    
    # Check positional arguments
    if args and len(args) > 1:
        if isinstance(args[1], str):
            return args[1]
        elif isinstance(args[1], list):
            return ' '.join(str(v) for v in args[1])
    
    return ""

def _estimate_tokens(text: str) -> int:
    """Rough estimation of token count (4 chars = 1 token approximation)."""
    return max(1, len(text) // 4)

# Convenience functions for manual tracking
def log_llm_usage(provider: str, model: str, input_tokens: int, output_tokens: int, 
                  operation: str = "manual", api_key: Optional[str] = None, **metadata):
    """Manually log LLM usage."""
    monitor = get_token_monitor()
    return monitor.log_usage(
        provider=provider,
        service_type=ServiceType.LLM,
        model=model,
        operation=operation,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        api_key=api_key,
        metadata=metadata
    )

def log_embedding_usage(provider: str, model: str, input_tokens: int, 
                       operation: str = "manual", api_key: Optional[str] = None, **metadata):
    """Manually log embedding usage."""
    monitor = get_token_monitor()
    return monitor.log_usage(
        provider=provider,
        service_type=ServiceType.EMBEDDING,
        model=model,
        operation=operation,
        input_tokens=input_tokens,
        output_tokens=0,
        api_key=api_key,
        metadata=metadata
    )

def get_usage_report(provider: Optional[str] = None, days: int = 30) -> Dict[str, Any]:
    """Get usage report for provider or all providers."""
    monitor = get_token_monitor()
    if provider:
        return monitor.get_provider_summary(provider, days)
    else:
        return monitor.get_comprehensive_report()

def set_provider_limit(provider: str, limit_type: str, value: int):
    """Set subscription limit for a provider."""
    monitor = get_token_monitor()
    return monitor.set_subscription_limit(provider, limit_type, value)