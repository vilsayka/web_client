CREATE TABLE importer (
    id_importer SERIAL PRIMARY KEY,
    user_name VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    telephone VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL, 
    is_active BOOLEAN DEFAULT TRUE,
    user_role VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id_order SERIAL PRIMARY KEY,
    id_customer INTEGER REFERENCES users(id_user) NOT NULL,
    id_importer INTEGER REFERENCES importer(id_importer) NOT NULL,
    date_order DATE NOT NULL,
    date_assembly DATE NOT NULL,
    warranty_period INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE components (
    id_component SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    manufacturer VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    warranty_period INTEGER DEFAULT 0,
    price_complete DECIMAL(10, 2) NOT NULL,
    quantity_accessories INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE component_specs (
    id_spec SERIAL PRIMARY KEY,
    id_component INTEGER UNIQUE REFERENCES components(id_component) ON DELETE CASCADE,
    specifications JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE service_guarantees (
    id_repair_warranty SERIAL PRIMARY KEY,
    id_order INTEGER REFERENCES orders(id_order) NOT NULL,
    id_defective_component INTEGER NOT NULL,
    date_references DATE,
    date_repair_completion DATE,
    Problem_description VARCHAR(300) NOT NULL,
    status_order VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE pc_composition (
    id_entry SERIAL PRIMARY KEY,
    id_order INTEGER REFERENCES orders(id_order) NOT NULL,
    id_component INTEGER REFERENCES components(id_component) NOT NULL,
    number_components INTEGER NOT NULL
);
