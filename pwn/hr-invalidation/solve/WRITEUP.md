# pwn - HR Invalidation

C'est un challenge de pwn en C++.

En regardant rapidement le code source, on peut déjà noter que les deux classes
ont chacune une méthode virtuelle (qui feront usage de la vtable donc) :
```cpp
class Employee {
    public:
        unsigned long id;
        std::string firstname;
        std::string lastname;
        double salary;

        Employee(std::string firstname, std::string lastname, double salary) : firstname(firstname), lastname(lastname), salary(salary) { this->id = g_id++; }
        virtual void print();
};

class Manager {
    private:
        virtual void get_flag();

    public:
        char firstname[88];
        char lastname[88];
};
```

De plus `Manager::get_flag` n'est jamais appelé dans le code, on peut donc se
douter qu'il pourrait y avoir une confusion de type entre `Manager` et
`Employee`.

La vulnérabilité est induite par la variable `g_last_employee`. Cette variable
de type `Employee*` est un pointeur vers un élément de `g_employees`.

En C++ un vecteur est simplement un tableau alloué sur le tas et pour lequel
certaines opérations sont définies. Tous ses éléments sont stockés les uns à la
suite des autres (ce n'est pas une liste chaînée).
Lorsque l'on ajoute un élément à un vecteur (via `add_employee` dans notre cas)
le vecteur peut être réalloué si sa taille n'est pas suffisante pour contenir
le nouvel élément.
Cette réallocation peut changer l'emplacement du vecteur, et invalider toutes
les anciennes références aux éléments du vecteur.

Voir https://en.cppreference.com/w/cpp/container/vector#Iterator_invalidation
et https://en.cppreference.com/w/cpp/container#Iterator_invalidation.

Solution :
- Créer deux `Employee` pour allouer un chunk de 0xc0 octets (la même taille
  que pour un `Manager`).
- Faire pointer `g_last_employee` vers le premier élément de `g_employees` en
  appelant `search_employee_by_id`.
- Créer un troisième `Employee` pour entraîner la réallocation de `g_employees`. 
- Logout pour allouer un `Manager`. Le chunk de 0xc0 octets contenant
  auparavant les deux `Employee` sera utilisé par le nouveau `Manager`. On a
  donc maintenant `g_last_employee` qui pointe vers le nouveau `Manager`.
- Afficher les données de `g_last_employee`. Cela va appeler la fonction de la
  vtable de `g_last_employee` ce qui va en réalité appeler `Manager::get_flag`
  car `g_last_employee` pointe vers le nouveau `Manager`.
