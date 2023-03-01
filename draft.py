a = {
    "Authorization": f"Bearer",
}

b = {
    "Content-Type": "application/json",
}
a.update(b)

print(a)
