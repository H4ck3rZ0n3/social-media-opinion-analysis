# gpu_resource_manager.py

import gc
import logging

import cupy as cp


class GPUResourceManager:
    @staticmethod
    def clear_gpu_memory():
        try:
            cp.get_default_memory_pool().free_all_blocks()
            cp.get_default_pinned_memory_pool().free_all_blocks()
            gc.collect()
            logging.info("GPU memory successfully cleared.")
        except Exception as e:
            logging.error(f"Failed to clear GPU memory: {e}")
