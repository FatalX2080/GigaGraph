from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json


class TaskResult:
    def __init__(self, success: bool, task_name: str, 
                 data: Dict[str, Any] = None, 
                 visualizations: List[str] = None,
                 metadata: Dict[str, Any] = None,
                 error: Optional[str] = None):
        self.success = success
        self.task_name = task_name
        self.data = data or {}
        self.visualizations = visualizations or []
        self.metadata = metadata or {}
        self.error = error

    def to_dict(self):
        return {
            'success': self.success,
            'task_name': self.task_name,
            'data': self.data,
            'visualizations': self.visualizations,
            'metadata': self.metadata,
            'error': self.error
        }
    
    def to_json(self):
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)