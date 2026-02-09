import asyncio
from sqlalchemy import text
from app.database import AsyncSessionMaker
from app.models import Building, Organisation, OrganisationPhone, Activity
from app.core.config import get_settings

print(f"DATABASE_URL: {get_settings().database_url}")


async def seed():
    async with AsyncSessionMaker() as session:

        building1 = Building(
            address="г. Москва, ул. Тверская 10",
            latitude=55.764680,
            longitude=37.605750
        )
        building2 = Building(
            address="г. Москва, Кутузовский проспект 32",
            latitude=55.740370,
            longitude=37.535080
        )
        building3 = Building(
            address="г. Москва, ул. Новый Арбат 15",
            latitude=55.752200,
            longitude=37.591900
        )
        building4 = Building(
            address="г. Химки, Ленинградское шоссе 25",
            latitude=55.895833,
            longitude=37.443889
        )
        building5 = Building(
            address="г. Подольск, ул. Кирова 12",
            latitude=55.423889,
            longitude=37.545556
        )
        building6 = Building(
            address="г. Москва, Ленинский проспект 42",
            latitude=55.707222,
            longitude=37.593611
        )

        session.add_all([building1, building2, building3, building4, building5, building6])
        await session.flush()

        food = Activity(name="Еда", level=1)
        auto = Activity(name="Автомобили", level=1)
        tech = Activity(name="Электроника", level=1)
        services = Activity(name="Услуги", level=1)
        session.add_all([food, auto, tech, services])
        await session.flush()

        meat = Activity(name="Мясная продукция", parent=food, level=2)
        dairy = Activity(name="Молочная продукция", parent=food, level=2)
        bakery = Activity(name="Хлебобулочные изделия", parent=food, level=2)

        truck = Activity(name="Грузовые", parent=auto, level=2)
        passenger = Activity(name="Легковые", parent=auto, level=2)
        moto = Activity(name="Мототехника", parent=auto, level=2)

        computers = Activity(name="Компьютеры", parent=tech, level=2)
        phones = Activity(name="Смартфоны", parent=tech, level=2)
        home_tech = Activity(name="Бытовая техника", parent=tech, level=2)

        repair = Activity(name="Ремонт", parent=services, level=2)
        consulting = Activity(name="Консалтинг", parent=services, level=2)

        session.add_all([
            meat, dairy, bakery,
            truck, passenger, moto,
            computers, phones, home_tech,
            repair, consulting
        ])
        await session.flush()

        parts = Activity(name="Запчасти", parent=passenger, level=3)
        accessories = Activity(name="Аксессуары", parent=passenger, level=3)

        components = Activity(name="Комплектующие", parent=computers, level=3)
        peripherals = Activity(name="Периферия", parent=computers, level=3)

        auto_repair = Activity(name="Ремонт автомобилей", parent=repair, level=3)
        tech_repair = Activity(name="Ремонт техники", parent=repair, level=3)

        session.add_all([
            parts, accessories,
            components, peripherals,
            auto_repair, tech_repair
        ])
        await session.flush()

        org1 = Organisation(name='Мясной Двор', building=building1)
        org1.activities.extend([meat, dairy])
        session.add(org1)
        await session.flush()
        session.add(OrganisationPhone(organisation=org1, phone_number="+74951234567"))
        session.add(OrganisationPhone(organisation=org1, phone_number="+74951234568"))

        org2 = Organisation(name='ИП Петров', building=building1)
        org2.activities.append(meat)
        session.add(org2)
        await session.flush()
        session.add(OrganisationPhone(organisation=org2, phone_number="+79161112233"))

        org3 = Organisation(name='Золотой Колос', building=building2)
        org3.activities.extend([bakery, dairy])
        session.add(org3)
        await session.flush()
        session.add(OrganisationPhone(organisation=org3, phone_number="+74952345678"))
        session.add(OrganisationPhone(organisation=org3, phone_number="+79162223344"))

        org4 = Organisation(name='Молочный завод №1', building=building5)
        org4.activities.append(dairy)
        session.add(org4)
        await session.flush()
        session.add(OrganisationPhone(organisation=org4, phone_number="+74964445566"))

        org5 = Organisation(name='Премиум Авто', building=building3)
        org5.activities.extend([passenger, parts, accessories])
        session.add(org5)
        await session.flush()
        session.add(OrganisationPhone(organisation=org5, phone_number="+74953334455"))

        org6 = Organisation(name='Экспресс', building=building4)
        org6.activities.append(truck)
        session.add(org6)
        await session.flush()
        session.add(OrganisationPhone(organisation=org6, phone_number="+74995556677"))
        session.add(OrganisationPhone(organisation=org6, phone_number="+79167778899"))

        org7 = Organisation(name='АвтоЗапчасти Плюс', building=building2)
        org7.activities.append(parts)
        session.add(org7)
        await session.flush()
        session.add(OrganisationPhone(organisation=org7, phone_number="+74956667788"))

        org8 = Organisation(name='Скорость', building=building6)
        org8.activities.extend([moto, accessories])
        session.add(org8)
        await session.flush()
        session.add(OrganisationPhone(organisation=org8, phone_number="+74951112233"))

        org9 = Organisation(name='ТехноМир', building=building3)
        org9.activities.extend([computers, phones, home_tech])
        session.add(org9)
        await session.flush()
        session.add(OrganisationPhone(organisation=org9, phone_number="+74952223344"))
        session.add(OrganisationPhone(organisation=org9, phone_number="+79163334455"))

        org10 = Organisation(name='КомпМастер', building=building1)
        org10.activities.extend([computers, components, peripherals])
        session.add(org10)
        await session.flush()
        session.add(OrganisationPhone(organisation=org10, phone_number="+74954445566"))

        org11 = Organisation(name='МобильныйМир', building=building2)
        org11.activities.append(phones)
        session.add(org11)
        await session.flush()
        session.add(OrganisationPhone(organisation=org11, phone_number="+74955556677"))
        session.add(OrganisationPhone(organisation=org11, phone_number="+79164445566"))

        org12 = Organisation(name='АвтоСервис+', building=building4)
        org12.activities.extend([auto_repair, parts])
        session.add(org12)
        await session.flush()
        session.add(OrganisationPhone(organisation=org12, phone_number="+74996667788"))

        org13 = Organisation(name='ТехРемонт', building=building6)
        org13.activities.extend([tech_repair, computers, phones])
        session.add(org13)
        await session.flush()
        session.add(OrganisationPhone(organisation=org13, phone_number="+74957778899"))
        session.add(OrganisationPhone(organisation=org13, phone_number="+79165556677"))

        org14 = Organisation(name='БизнесКонсалт', building=building3)
        org14.activities.append(consulting)
        session.add(org14)
        await session.flush()
        session.add(OrganisationPhone(organisation=org14, phone_number="+74958889900"))

        org15 = Organisation(name='Золотые Руки', building=building5)
        org15.activities.extend([repair, auto_repair, tech_repair])
        session.add(org15)
        await session.flush()
        session.add(OrganisationPhone(organisation=org15, phone_number="+74969991122"))
        session.add(OrganisationPhone(organisation=org15, phone_number="+79166667788"))

        await session.commit()
        print(f"Создано 15 организаций с телефонами")
        print("Заполнение БД завершено!")
        print()
        print("Статистика:")
        print(f"  • Зданий: 6 (Москва и МО)")
        print(f"  • Видов деятельности: 22 (уровни 1-3)")
        print(f"    - Еда (3 подтипа)")
        print(f"    - Автомобили (3 подтипа + 2 подподтипа)")
        print(f"    - Электроника (3 подтипа + 2 подподтипа)")
        print(f"    - Услуги (2 подтипа + 2 подподтипа)")
        print(f"  • Организаций: 15")
        print(f"  • Телефонов: 22")


async def clear():

    async with AsyncSessionMaker() as session:

        await session.execute(text(
            "TRUNCATE TABLE organisation_activities, organisation_phones, organisations, activities, buildings CASCADE"))

        await session.commit()
        print("БД очищена")


async def main():
    await clear()

    await seed()


if __name__ == "__main__":
    asyncio.run(main())