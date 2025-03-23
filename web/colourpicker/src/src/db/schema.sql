CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS jwt_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kid TEXT NOT NULL UNIQUE,
    kty TEXT NOT NULL, 
    p key TEXT NOT NULL,
    q key TEXT NOT NULL,
    d key TEXT NOT NULL,
    e key TEXT NOT NULL,
    n key TEXT NOT NULL,
    qi key TEXT NOT NULL,
    dp key TEXT NOT NULL,
    dq key TEXT NOT NULL
);

INSERT INTO jwt_keys (kid, kty, p, q, d, e,n ,qi, dp, dq) VALUES (
    'default',
    'RSA',
    '9CgncwPxNHq5UrfwoOehxxS9KP2cGHIOHBNdhQ1_JstaMRCXiTQSmGdCWBRKpgVTlVuC-BnTnfv8_iAsMWQ62w',
    '0jmpPEaBvRWdGnMA3Ze8LRy7BRgp1EZ9arE3eet-9mWdIjlLQkbRq_s4W_B701XCvog3R4AYJicZBD6pMwX8OQ',
    'RDt9YficFR77ffWSe2pUoASMpj385D9G7ZACsw4cArrZZmeuvAhkPFZIhGBSqp_BJSLSKn5gDLevvxYMJ1B_a0YrGbdSl5KnkQA4Bqy5bQplgbseKrc1dUZ99OTH6pRVfCX3r_jYRVlz95FJFWe_tPrN6GZi_UJG4mhikCztTlE',
    'AQAB',
    'yH_utSCKoawZ0GCbMpgWbruhrjxvReqGshuS5lUW1wVcofKs4e2pKenD0MPatNtHQYGR-_0i_KJDIkKiV2cvydM4Fx7LWU3Q-rN49b_sw4XqjuE2v5HuAUIwF4wBCBR90ZcIEZv_SMprjxGNFnbX5h0CuKIlj8VVGsx9t3CHrsM',
    'und1FyMS6r8Alb9SFTCkmy_yzGOrhPU2tcG0HtsZpuNwZTzb5w5SyIQi1HtX7iPimDXXTtusLuUxTKIDlmO5qg',
    'mkDoM40xDePfQ_h8KVxOZFWg8M3RmcwtR-WgNxiA1cSyFb-SzZc9jFXon3cqdlt1JC6tvwuqG-0BOJig8w-M8w',
    'xvJkkzNScmPy8mXlas---J5Y6uBMLaSr6f1eN9ZCp-HQC-RWsZkdsfkkA_YY6Q4fJ3r3fYXe1LRpe1flffDrGQ'
);