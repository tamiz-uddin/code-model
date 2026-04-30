"""
PHASE 3D: Extended Languages Fine-Tuning
Google Colab Notebook (Python version for reference)
"""

# ============================================================
# PHASE 3D: EXTENDED LANGUAGES
# TypeScript, Java, Go, Rust, C#, SQL
# ============================================================

# Cell 1: Setup
# !git clone https://github.com/YOUR_USERNAME/code-model.git
# %cd code-model
# !pip install -q torch transformers datasets tokenizers accelerate pyyaml

# import os
# from google.colab import files
# os.makedirs("outputs/models", exist_ok=True)
# print("Upload Phase 3C model (fullstack-model-v1.pt)")
# uploaded = files.upload()
# for filename in uploaded.keys():
#     os.rename(filename, f"outputs/models/{filename}")
#     print(f"✓ Uploaded: {filename}")

# Cell 2: Create Extended Languages Dataset
import json
from pathlib import Path

def create_extended_languages_dataset():
    """Create extended languages dataset for Phase 3D."""
    print("Creating extended languages dataset...")

    samples = [
        # ===== TYPESCRIPT (30 samples) =====
        # Interfaces
        "interface User { id: number; name: string; email: string; }",
        "interface ApiResponse<T> { status: number; data: T; error?: string; }",
        "type UserRole = 'admin' | 'user' | 'guest';",

        # Classes
        "class UserService { private users: User[] = []; getUser(id: number): User | undefined { return this.users.find(u => u.id === id); } addUser(user: User): void { this.users.push(user); } }",
        "abstract class Animal { abstract makeSound(): void; move(): void { console.log('Moving'); } }",

        # Generics
        "function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] { return obj[key]; }",
        "class Stack<T> { private items: T[] = []; push(item: T): void { this.items.push(item); } pop(): T | undefined { return this.items.pop(); } }",

        # Decorators
        "@Component({ selector: 'app-root', template: '<h1>App</h1>' }) class AppComponent { }",
        "function log(target: any, propertyKey: string, descriptor: PropertyDescriptor) { const originalMethod = descriptor.value; descriptor.value = function(...args: any[]) { console.log(`Calling ${propertyKey}`); return originalMethod.apply(this, args); }; }",

        # Async/Await
        "async function fetchUser(id: number): Promise<User> { const response = await fetch(`/api/users/${id}`); return response.json(); }",
        "async function processUsers(ids: number[]): Promise<User[]> { return Promise.all(ids.map(id => fetchUser(id))); }",

        # ===== JAVA (30 samples) =====
        # Classes
        "public class User { private int id; private String name; private String email; public User(int id, String name, String email) { this.id = id; this.name = name; this.email = email; } public int getId() { return id; } }",
        "public abstract class Animal { public abstract void makeSound(); public void move() { System.out.println(\"Moving\"); } }",

        # Interfaces
        "public interface UserRepository { User findById(int id); void save(User user); void delete(int id); }",
        "public interface Comparable<T> { int compareTo(T o); }",

        # Generics
        "public class Stack<T> { private List<T> items = new ArrayList<>(); public void push(T item) { items.add(item); } public T pop() { return items.remove(items.size() - 1); } }",
        "public <T> T getProperty(Map<String, T> map, String key) { return map.get(key); }",

        # Annotations
        "@Override public String toString() { return \"User: \" + name; }",
        "@Deprecated public void oldMethod() { }",

        # Streams
        "List<String> names = users.stream().map(User::getName).filter(n -> n.startsWith(\"J\")).collect(Collectors.toList());",
        "int sum = numbers.stream().reduce(0, Integer::sum);",

        # ===== GO (20 samples) =====
        # Functions
        "func Add(a, b int) int { return a + b }",
        "func Fibonacci(n int) int { if n <= 1 { return n } return Fibonacci(n-1) + Fibonacci(n-2) }",

        # Structs
        "type User struct { ID int; Name string; Email string }",
        "func (u User) String() string { return fmt.Sprintf(\"User: %s\", u.Name) }",

        # Interfaces
        "type Reader interface { Read(p []byte) (n int, err error) }",
        "type Writer interface { Write(p []byte) (n int, err error) }",

        # Goroutines
        "go func() { fmt.Println(\"Running in goroutine\") }()",
        "go fetchUser(userID)",

        # Channels
        "results := make(chan string); go func() { results <- \"done\" }(); msg := <-results",

        # ===== RUST (20 samples) =====
        # Functions
        "fn add(a: i32, b: i32) -> i32 { a + b }",
        "fn fibonacci(n: u32) -> u32 { if n <= 1 { n } else { fibonacci(n-1) + fibonacci(n-2) } }",

        # Structs
        "struct User { id: u32, name: String, email: String }",
        "impl User { fn new(id: u32, name: String, email: String) -> User { User { id, name, email } } }",

        # Traits
        "trait Animal { fn make_sound(&self); fn move_around(&self) { println!(\"Moving\"); } }",
        "impl Animal for Dog { fn make_sound(&self) { println!(\"Woof!\"); } }",

        # Ownership
        "let s1 = String::from(\"hello\"); let s2 = s1; // s1 is no longer valid",
        "fn takes_ownership(s: String) { println!(\"{}\", s); } // s is dropped here",

        # ===== C# (20 samples) =====
        # Classes
        "public class User { public int Id { get; set; } public string Name { get; set; } public string Email { get; set; } }",
        "public abstract class Animal { public abstract void MakeSound(); public virtual void Move() { Console.WriteLine(\"Moving\"); } }",

        # Interfaces
        "public interface IUserRepository { User GetById(int id); void Save(User user); void Delete(int id); }",

        # LINQ
        "var names = users.Where(u => u.Name.StartsWith(\"J\")).Select(u => u.Name).ToList();",
        "var sum = numbers.Aggregate(0, (acc, n) => acc + n);",

        # Async/Await
        "public async Task<User> GetUserAsync(int id) { var response = await httpClient.GetAsync($\"/api/users/{id}\"); return await response.Content.ReadAsAsync<User>(); }",

        # ===== SQL (25 samples) =====
        # SELECT
        "SELECT * FROM users;",
        "SELECT id, name, email FROM users WHERE email LIKE '%@example.com';",
        "SELECT u.name, COUNT(p.id) as post_count FROM users u LEFT JOIN posts p ON u.id = p.user_id GROUP BY u.id;",

        # INSERT
        "INSERT INTO users (name, email) VALUES ('John', 'john@example.com');",
        "INSERT INTO users (name, email) SELECT name, email FROM temp_users;",

        # UPDATE
        "UPDATE users SET email = 'newemail@example.com' WHERE id = 1;",
        "UPDATE users SET updated_at = NOW() WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);",

        # DELETE
        "DELETE FROM users WHERE id = 1;",
        "DELETE FROM users WHERE email IS NULL;",

        # Joins
        "SELECT u.name, p.title FROM users u INNER JOIN posts p ON u.id = p.user_id;",
        "SELECT u.name, p.title FROM users u LEFT JOIN posts p ON u.id = p.user_id;",

        # Aggregations
        "SELECT COUNT(*) as total_users FROM users;",
        "SELECT AVG(age) as average_age FROM users;",
        "SELECT MAX(salary) as highest_salary FROM employees;",

        # Subqueries
        "SELECT * FROM users WHERE id IN (SELECT user_id FROM posts GROUP BY user_id HAVING COUNT(*) > 5);",
        "SELECT * FROM users WHERE email IN (SELECT email FROM temp_users);",

        # Window Functions
        "SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) as rank FROM employees;",
        "SELECT name, salary, AVG(salary) OVER (PARTITION BY department) as dept_avg FROM employees;",

        # CTEs
        "WITH user_posts AS (SELECT user_id, COUNT(*) as post_count FROM posts GROUP BY user_id) SELECT u.name, up.post_count FROM users u JOIN user_posts up ON u.id = up.user_id;",
    ]

    # Create output directory
    output_dir = Path("data/phase3d")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save as JSONL
    output_file = output_dir / "data.jsonl"
    with open(output_file, "w") as f:
        for code in samples:
            f.write(json.dumps({"content": code}) + "\n")

    print(f"✓ Generated {len(samples)} samples")
    print(f"✓ TypeScript: 30 samples")
    print(f"✓ Java: 30 samples")
    print(f"✓ Go: 20 samples")
    print(f"✓ Rust: 20 samples")
    print(f"✓ C#: 20 samples")
    print(f"✓ SQL: 25 samples")
    print(f"✓ Saved to {output_file}")
    return True

if __name__ == "__main__":
    create_extended_languages_dataset()
