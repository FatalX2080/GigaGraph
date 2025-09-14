from typing import Any, Dict, List, Optional
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
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)