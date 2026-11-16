
from recommender import recommend_news

# Tester un utilisateur connu
print("TEST UTILISATEUR CONNU")

result = recommend_news("U100", top_n=10)

print(result.to_string(index=False))


# Tester un utilisateur inconnu
print("\nTEST UTILISATEUR INCONNU")

result_unknown = recommend_news(
    "U_UNKNOWN",
    top_n=10
)

print(result_unknown.to_string(index=False))
