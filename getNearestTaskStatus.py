from config import PERSONAL_ACCESS_TOKEN, PROJECT_GID, WORKSPACE_GID, AP, RK
import asana


def get_tasks(client):
    params = {
        'project': PROJECT_GID,
        'limit': 100,
        'opt_fields': ['assignee', 'due_on']
    }

    return client.tasks.get_tasks(params)


def get_tasks_by_user(client, user_gid):
    params = {
        'workspace': WORKSPACE_GID,
        'assignee': user_gid,
        'limit': 100,
        'opt_fields': ['assignee', 'due_on', 'projects']
    }

    return client.tasks.get_tasks(params)


def main():
    client = asana.Client.access_token(PERSONAL_ACCESS_TOKEN)
    tasks = get_tasks(client, AP.gid)
    for task in tasks:
        print(task)


if __name__ == '__main__':
    main()
