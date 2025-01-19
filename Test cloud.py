from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Définition de la base
Base = declarative_base()

class House(Base):
    __tablename__ = "houses"
    
    # Définition des colonnes de la table
    id = Column(Integer, primary_key=True, autoincrement=True)
    longitude = Column(Float)
    latitude = Column(Float)
    housing_median_age = Column(Integer)
    total_rooms = Column(Integer)
    total_bedrooms = Column(Integer)
    population = Column(Integer)
    households = Column(Integer)
    median_income = Column(Float)
    median_house_value = Column(Float)
    ocean_proximity = Column(String)

# Configuration de l'URL de connexion à la base de données
DATABASE_URL = "postgresql://kevin:KV1292005@localhost:5432/housing_db"

# Créer un moteur de base de données
engine = create_engine(DATABASE_URL)

# Créer toutes les tables définies (si elles ne sont pas encore créées)
Base.metadata.create_all(engine)

# Créer un objet Session pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Créer une instance de la session
session = SessionLocal()

try:
    # Exemple d'ajout d'une nouvelle maison
    new_house = House(
        longitude=-122.23,
        latitude=37.88,
        housing_median_age=41,
        total_rooms=880,
        total_bedrooms=129,
        population=322,
        households=126,
        median_income=8.3252,
        median_house_value=452600.0,
        ocean_proximity="NEAR BAY"
    )

    # Ajouter la maison à la session
    session.add(new_house)

    # Valider (commit) les changements dans la base de données
    session.commit()
    print("Nouvelle maison ajoutée avec succès !")

except Exception as e:
    # Si quelque chose échoue, annule les changements
    session.rollback()
    print(f"Erreur : {e}")

finally:
    # Toujours fermer la session à la fin
    session.close()
