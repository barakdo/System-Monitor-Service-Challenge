from src.tasks import task
from src.logic.helpers.preferences_validator import validate_user_preferences

def main():
  validate_user_preferences()
  task()

if __name__ == '__main__':
  main()