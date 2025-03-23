#include <iostream>
#include <vector>
#include <limits>
#include <algorithm>
#include <iomanip>


unsigned long g_id = 0;

class Employee {
    public:
        unsigned long id;
        std::string firstname;
        std::string lastname;
        double salary;

        Employee(std::string firstname, std::string lastname, double salary) : firstname(firstname), lastname(lastname), salary(salary) { this->id = g_id++; }
        virtual void print();
};

void Employee::print() {
    std::cout << this->id << ": " << this->firstname << " " << this->lastname << ", salary: " << this->salary << std::endl;
}

class Manager {
    private:
        virtual void get_flag();

    public:
        char firstname[88];
        char lastname[88];
};

void Manager::get_flag() {
    const char *flag = std::getenv("FLAG");

    if (flag == nullptr) {
        flag = "BZHCTF{fake_flag}";
    }


    std::cout << "Congrats! Here is the flag: " << flag << std::endl;
}

std::vector<Employee> g_employees = {};
Employee *g_last_employee = NULL;
Manager *g_current_user = NULL;


void list_employees() {
    for (auto employee: g_employees) {
        employee.print();
    }
}

void add_employee() {
    std::string firstname;
    std::string lastname;
    double salary;

    std::cout << "First name: ";
    std::cin >> firstname;

    std::cout << "Last name: ";
    std::cin >> lastname;

    std::cout << "Salary: ";
    std::cin >> salary;

    g_employees.emplace_back(firstname, lastname, salary);
}

void remove_employee() {
    int id;

    std::cout << "Enter the id of the employee to be deleted.\n> ";
    std::cin >> id;

    if (id == -1 && g_last_employee != NULL) {
        id = g_last_employee->id;
    }

    auto it = g_employees.begin();
    for (; it != g_employees.end(); it++) {
        if ((*it).id == id) {
            break;
        }
    }

    if (it == g_employees.end()) {
        std::cout << "No such employee.\n";
        return;
    }

    g_employees.erase(it);

    Employee *employee = &*it;
    if (employee == g_last_employee) {
        g_last_employee = NULL;
    }
}

Employee *do_search_employee_by_id(unsigned long id) {
    Employee *employee = NULL;

    if (id == -1 && g_last_employee != NULL) {
        employee = g_last_employee;
    } else {
        auto it = std::find_if(g_employees.begin(), g_employees.end(), [id](const Employee& employee) {
            return employee.id == id;
        });

        if (it == g_employees.end()) {
            return NULL;
        }

        employee = &*it;
    }

    g_last_employee = employee;
    return employee;
}

void search_employee_by_id() {
    int id;
    std::cout << "You can search an employee by its id.\nType -1 to display information about the last employee you searched for.\n> ";
    std::cin >> id;

    Employee *employee = do_search_employee_by_id(id);

    if (employee == NULL) {
        std::cout << "No such employee.\n";
        return;
    }

    employee->print();
}

Employee *do_search_employee_by_lastname(std::string lastname) {
    Employee *employee = NULL;

    if (lastname == "" && g_last_employee != NULL) {
        employee = g_last_employee;
    } else {
        auto it = std::find_if(g_employees.begin(), g_employees.end(), [lastname](const Employee& employee) {
            return employee.lastname == lastname;
        });

        if (it == g_employees.end()) {
            return NULL;
        }

        employee = &*it;
    }

    g_last_employee = employee;
    return employee;
}

void search_employee_by_lastname() {
    std::string lastname;

    std::cout << "You can search an employee by its lastname.\nPress Enter to display information about the last employee you searched for.\n> ";
    std::getline(std::cin, lastname);

    Employee *employee = do_search_employee_by_lastname(lastname);

    if (employee == NULL) {
        std::cout << "No such employee.\n";
        return;
    }

    employee->print();
}

void logout() {
    g_current_user = NULL;
}

void do_exit() {
    std::cout << "Bye!\n";
    exit(EXIT_SUCCESS);
}

const std::vector<std::pair<std::string, void(*)()>> actions = {
    { "List employees", list_employees },
    { "Search for an employee by its id", search_employee_by_id },
    { "Search for an employee by its lastname", search_employee_by_lastname },
    { "Add an employee", add_employee },
    { "Remove an employee", remove_employee },
    { "Logout", logout },
    { "Exit", do_exit },
};

void menu() {
    std::cout << "Menu:\n";
    int i = 0;
    for (auto action: actions) {
        std::cout << i << ": " << action.first << std::endl;
        i++;
    }
}

int main() {
    int choice;

    while (1) {
        if (g_current_user == NULL) {
            g_current_user = new Manager();

            std::cout << "First name: ";
            std::cin >> std::setw(sizeof(g_current_user->firstname)) >> g_current_user->firstname;

            std::cout << "Last name: ";
            std::cin >> std::setw(sizeof(g_current_user->lastname)) >> g_current_user->lastname;

            std::cout << "Hello " << g_current_user->firstname << " " << g_current_user->lastname << "!\n";
            continue;
        }

        menu();
        std::cout << "> ";
        std::cin >> choice;
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        if (choice < 0 || choice >= actions.size()) {
            std::cout << "Unknown choice\n";
            continue;
        }

        (*actions.at(choice).second)();
        std::cout << std::endl;
    }

    return 0;
}
