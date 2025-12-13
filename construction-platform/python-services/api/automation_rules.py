# Automation Rules
# construction-platform/python-services/api/automation_rules.py

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
import json
from enum import Enum

logger = logging.getLogger(__name__)

class RuleTrigger(Enum):
    """Rule trigger types"""
    FILE_UPLOAD = "file_upload"
    FILE_PROCESSED = "file_processed"
    ERROR_OCCURRED = "error_occurred"
    USAGE_THRESHOLD = "usage_threshold"
    SCHEDULED = "scheduled"
    MANUAL = "manual"

class RuleAction(Enum):
    """Rule action types"""
    SEND_NOTIFICATION = "send_notification"
    ARCHIVE_FILE = "archive_file"
    DELETE_FILE = "delete_file"
    RUN_WORKFLOW = "run_workflow"
    SEND_EMAIL = "send_email"
    CREATE_ALERT = "create_alert"

class AutomationRule:
    """Automation rule definition"""
    def __init__(
        self,
        rule_id: str,
        name: str,
        trigger: RuleTrigger,
        condition: Dict[str, Any],
        action: RuleAction,
        action_params: Dict[str, Any],
        enabled: bool = True
    ):
        self.rule_id = rule_id
        self.name = name
        self.trigger = trigger
        self.condition = condition
        self.action = action
        self.action_params = action_params
        self.enabled = enabled
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.execution_count = 0
        self.last_executed = None

class AutomationRuleEngine:
    """Automation rule engine"""
    def __init__(self):
        self.rules: Dict[str, AutomationRule] = {}
        self.rule_executions: List[Dict[str, Any]] = []
    
    def add_rule(self, rule: AutomationRule) -> bool:
        """Add automation rule"""
        try:
            self.rules[rule.rule_id] = rule
            logger.info(f"Automation rule added: {rule.rule_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add automation rule: {e}")
            return False
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove automation rule"""
        try:
            if rule_id in self.rules:
                del self.rules[rule_id]
                logger.info(f"Automation rule removed: {rule_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove automation rule: {e}")
            return False
    
    def evaluate_rule(self, rule: AutomationRule, context: Dict[str, Any]) -> bool:
        """Evaluate rule condition"""
        try:
            condition = rule.condition
            condition_type = condition.get("type")
            
            if condition_type == "equals":
                return context.get(condition.get("field")) == condition.get("value")
            elif condition_type == "greater_than":
                return context.get(condition.get("field")) > condition.get("value")
            elif condition_type == "less_than":
                return context.get(condition.get("field")) < condition.get("value")
            elif condition_type == "contains":
                return condition.get("value") in str(context.get(condition.get("field"), ""))
            elif condition_type == "regex":
                import re
                return bool(re.search(condition.get("pattern"), str(context.get(condition.get("field"), ""))))
            else:
                return False
        except Exception as e:
            logger.error(f"Failed to evaluate rule condition: {e}")
            return False
    
    def execute_rule(self, rule: AutomationRule, context: Dict[str, Any]) -> bool:
        """Execute rule action"""
        try:
            action = rule.action
            action_params = rule.action_params
            
            if action == RuleAction.SEND_NOTIFICATION:
                # Send notification
                logger.info(f"Sending notification: {action_params.get('message')}")
                return True
            elif action == RuleAction.ARCHIVE_FILE:
                # Archive file
                file_id = context.get("file_id")
                logger.info(f"Archiving file: {file_id}")
                return True
            elif action == RuleAction.DELETE_FILE:
                # Delete file
                file_id = context.get("file_id")
                logger.info(f"Deleting file: {file_id}")
                return True
            elif action == RuleAction.RUN_WORKFLOW:
                # Run workflow
                workflow_id = action_params.get("workflow_id")
                logger.info(f"Running workflow: {workflow_id}")
                return True
            elif action == RuleAction.SEND_EMAIL:
                # Send email
                email = action_params.get("email")
                subject = action_params.get("subject")
                logger.info(f"Sending email to: {email}, subject: {subject}")
                return True
            elif action == RuleAction.CREATE_ALERT:
                # Create alert
                alert_message = action_params.get("message")
                logger.info(f"Creating alert: {alert_message}")
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Failed to execute rule action: {e}")
            return False
    
    def process_trigger(self, trigger: RuleTrigger, context: Dict[str, Any]) -> int:
        """Process trigger and execute matching rules"""
        executed_count = 0
        try:
            for rule in self.rules.values():
                if not rule.enabled:
                    continue
                
                if rule.trigger != trigger:
                    continue
                
                if self.evaluate_rule(rule, context):
                    if self.execute_rule(rule, context):
                        rule.execution_count += 1
                        rule.last_executed = datetime.now()
                        executed_count += 1
                        
                        # Log execution
                        self.rule_executions.append({
                            "rule_id": rule.rule_id,
                            "rule_name": rule.name,
                            "trigger": trigger.value,
                            "context": context,
                            "executed_at": datetime.now().isoformat()
                        })
            
            logger.info(f"Processed trigger {trigger.value}: {executed_count} rules executed")
            return executed_count
        except Exception as e:
            logger.error(f"Failed to process trigger: {e}")
            return executed_count
    
    def get_rules(self, tenant_id: str = None) -> List[Dict[str, Any]]:
        """Get automation rules"""
        rules = []
        for rule in self.rules.values():
            rules.append({
                "rule_id": rule.rule_id,
                "name": rule.name,
                "trigger": rule.trigger.value,
                "condition": rule.condition,
                "action": rule.action.value,
                "action_params": rule.action_params,
                "enabled": rule.enabled,
                "execution_count": rule.execution_count,
                "last_executed": rule.last_executed.isoformat() if rule.last_executed else None
            })
        return rules
    
    def get_rule_executions(self, rule_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get rule executions"""
        executions = self.rule_executions
        if rule_id:
            executions = [e for e in executions if e["rule_id"] == rule_id]
        return executions[-limit:]

# Global automation rule engine instance
automation_engine = AutomationRuleEngine()
