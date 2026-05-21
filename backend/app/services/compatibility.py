# app/services/compatibility.py

def get_category(comp: dict) -> str:
    """Определяем категорию по полю title."""
    title = comp.get("title", "")
    mapping = {
        "Processor": "processor",
        "Motherboard": "motherboard",
        "Graphics Card": "gpu",
        "RAM": "ram",
        "Storage": "storage",
        "Power Supply": "psu",
        "CPU Cooler": "cooler",
        "Case": "case"
    }
    return mapping.get(title, "unknown")

def perform_compatibility_check(components: list[dict]) -> list[str]:
    conflicts = []
    # группируем по категориям
    cats = {}
    for comp in components:
        cat = get_category(comp)
        if cat == "unknown":
            conflicts.append(f"Неизвестный тип компонента: {comp['title']}")
            continue
        if cat in cats:
            conflicts.append(f"Дублирование компонента категории {cat}")
        else:
            cats[cat] = comp

    # Процессор и материнская плата
    if "processor" in cats and "motherboard" in cats:
        p_socket = cats["processor"]["specifications"].get("socket")
        m_socket = cats["motherboard"]["specifications"].get("socket")
        if p_socket and m_socket and p_socket != m_socket:
            conflicts.append(f"Сокет процессора ({p_socket}) не совпадает с сокетом материнской платы ({m_socket})")

    # Процессор и кулер
    if "processor" in cats and "cooler" in cats:
        p_socket = cats["processor"]["specifications"].get("socket")
        c_sockets = cats["cooler"]["specifications"].get("supported_sockets", [])
        if p_socket and c_sockets and p_socket not in c_sockets:
            conflicts.append(f"Кулер не поддерживает сокет процессора ({p_socket})")
        p_tdp = cats["processor"]["specifications"].get("tdp_w")
        c_tdp = cats["cooler"]["specifications"].get("tdp_w")
        if p_tdp and c_tdp and c_tdp < p_tdp:
            conflicts.append(f"Кулер рассчитан на {c_tdp}W, а процессор на {p_tdp}W")

    # Материнская плата и оперативная память
    if "motherboard" in cats and "ram" in cats:
        m_ram = cats["motherboard"]["specifications"].get("ram_type")
        r_type = cats["ram"]["specifications"].get("type")
        if m_ram and r_type and m_ram != r_type:
            conflicts.append(f"Тип памяти: материнская плата {m_ram}, память {r_type}")

    # Корпус и материнская плата
    if "case" in cats and "motherboard" in cats:
        mb_form = cats["motherboard"]["specifications"].get("form_factor")
        case_forms = cats["case"]["specifications"].get("form_factors_supported", [])
        if mb_form and case_forms and mb_form not in case_forms:
            conflicts.append(f"Форм-фактор платы ({mb_form}) не поддерживается корпусом")

    # Блок питания и суммарное TDP
    if "psu" in cats:
        total_tdp = 0
        for c in [cats.get("processor"), cats.get("gpu")]:
            if c:
                tdp = c["specifications"].get("tdp_w", 0)
                total_tdp += tdp
        psu_watt = cats["psu"]["specifications"].get("wattage", 0)
        if total_tdp > psu_watt * 0.8:  # запас 20%
            conflicts.append(f"Блок питания ({psu_watt}W) недостаточен для потребления {total_tdp}W")

    # Можно добавить другие проверки по аналогии

    return conflicts