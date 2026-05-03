"""ЃЁ§­Ґб-«®ЈЁЄ :  «Ј®аЁв¬л  ­ «Ё§  § Јаг§ЄЁ Ё Ї®¤Ў®а  ЁбЇ®«­ЁвҐ«Ґ©."""

from sqlalchemy.orm import Session

from app.models import Task, User, TaskStatus





def calculate_workload(db: Session, project_id: int) -> list[dict]:

    """Џ®¤бзЁвлў Ґв § Јаг§Єг Є ¦¤®Ј® ЁбЇ®«­ЁвҐ«п ў Їа®ҐЄвҐ."""

    tasks = db.query(Task).filter(Task.project_id == project_id, Task.assignee_id.isnot(None), Task.status != TaskStatus.DONE).all()

    workload = {}

    for task in tasks:

        uid = task.assignee_id

        if uid not in workload:

            user = db.query(User).filter(User.id == uid).first()

            workload[uid] = {"user_id": uid, "username": user.username if user else "unknown", "total_hours": 0, "task_count": 0}

        workload[uid]["total_hours"] += task.estimated_hours

        workload[uid]["task_count"] += 1

    result = list(workload.values())

    result.sort(key=lambda x: (x["total_hours"], x["task_count"]))

    return result





def suggest_task_assignment(db: Session, project_id: int) -> dict:

    """Ђ«Ј®аЁв¬ Ї®¤Ў®а  ®ЇвЁ¬ «м­®Ј® ЁбЇ®«­ЁвҐ«п ¤«п ­®ў®© § ¤ зЁ."""

    workload = calculate_workload(db, project_id)

    all_users = db.query(User).all()

    all_user_ids = {u.id for u in all_users}

    busy_ids = {w["user_id"] for w in workload}

    free_ids = all_user_ids - busy_ids

    if free_ids:

        free_user = db.query(User).filter(User.id == list(free_ids)[0]).first()

        return {"suggested_user_id": free_user.id, "suggested_username": free_user.username, "reason": "“ нв®Ј® Ї®«м§®ў вҐ«п ­Ґв  ЄвЁў­ле § ¤ з. ЋЇвЁ¬ «м­® ­ §­ зЁвм § ¤ зг ­  бў®Ў®¤­®Ј® ЁбЇ®«­ЁвҐ«п."}

    if workload:

        best = workload[0]

        return {"suggested_user_id": best["user_id"], "suggested_username": best["username"], "reason": f"Ќ Ё¬Ґ­ми п § Јаг§Є : {best['total_hours']} з б®ў, {best['task_count']} § ¤ з^(Ё^). ‚лЎа ­ Ї® ¬Ё­Ё¬ «м­л¬ бг¬¬ а­л¬ з б ¬."}

    return {"message": "ЌҐв Ї®«м§®ў вҐ«Ґ© ¤«п ­ §­ зҐ­Ёп"}

