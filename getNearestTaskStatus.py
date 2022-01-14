from config import PERSONAL_ACCESS_TOKEN, PROJECT_GID, WORKSPACE_GID, AP, RK
import asana
from datetime import datetime, date
from colour import Color

URGENT_COLOR = Color('red')
ON_TRACK_COLOR = Color('green')


def get_tasks(client):
    params = {
        'project': PROJECT_GID,
        'limit': 100,
        'opt_fields': ['name', 'assignee', 'due_on']
    }

    return client.tasks.get_tasks(params)


def get_tasks_by_user(client, user_gid):
    params = {
        'workspace': WORKSPACE_GID,
        'assignee': user_gid,
        'limit': 100,
        'opt_fields': ['name', 'assignee', 'due_on', 'projects']
    }

    return client.tasks.get_tasks(params)


def filter_tasks_by_project(tasks, project_gid=PROJECT_GID):
    def part_of_project(task, project_gid):
        return project_gid in map(lambda project: project['gid'], task['projects'])

    return filter(lambda task: part_of_project(task, project_gid), tasks)


def filter_tasks_by_date_proximity(tasks, days_within):
    today = date.today()

    def proximal(task, days_within):
        due_date = datetime.strptime(task['due_on'], "%Y-%m-%d").date()
        return (due_date - today).days <= days_within

    return filter(lambda task: proximal(task, days_within), tasks)


def get_days_to_nearest_task(tasks):
    nearest_proximity = None
    today = date.today()
    for task in tasks:
        due_date = datetime.strptime(task['due_on'], "%Y-%m-%d").date()
        proximity = (due_date - today).days
        nearest_proximity = min(
            proximity, nearest_proximity) if nearest_proximity is not None else proximity
    return nearest_proximity


def get_color_range(color_1, color_2, range_size=6):
    return list(color_1.range_to(color_2, range_size))


def get_status_color(color_range, proximity):
    idx = proximity + 3  # 3 days overdue -> worst case
    # ensure index is within list indices range
    idx = min(max(idx, 0), len(color_range) - 1)

    return color_range[idx]


def main():
    color_range = get_color_range(URGENT_COLOR, ON_TRACK_COLOR)

    client = asana.Client.access_token(PERSONAL_ACCESS_TOKEN)
    tasks = get_tasks_by_user(client, AP.gid)
    tasks = filter_tasks_by_project(tasks)
    proximity = get_days_to_nearest_task(tasks)
    return get_status_color(color_range, proximity)


if __name__ == '__main__':
    main()
