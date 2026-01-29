import pandas as pd

# Load Biden tweets
file = pd.read_csv('/Users/adrian/Desktop/hashtag_joebiden.csv')

# Republican hashtags (supporting Trump/attacking Biden)
republican_tags = [
    'maga', 'trump2020', 'trump2024', 'kag', 'makeamericagreatagain',
    'trumptrain', 'draintheswamp', 'walkaway', 'votetrump',
    'sleepyjoe', 'corruptjoe', 'crookedjoe', 'bidencrimeFamily'
]

# Democrat hashtags (supporting Biden)
democrat_tags = [
    'biden2020', 'votebiden', 'ridinwithbiden', 'bidenharris',
    'settleforbiden', 'teamjoe', 'joebiden2020', 'voteblue'
]

# Negative words (attacking Biden = Republican)
negative_words = [
    'corrupt', 'criminal', 'crook', 'liar', 'fraud', 'terrible',
    'worst', 'disaster', 'dementia', 'senile', 'sleepy', 'creepy'
]

# Positive words (supporting Biden = Democrat)
positive_words = [
    'great', 'best', 'amazing', 'hope', 'president', 'leader',
    'experienced', 'qualified', 'respect'
]


def classify_tweet(tweet):
    if not isinstance(tweet, str):
        return None, 0, 0

    tweet_lower = tweet.lower()
    republican_score = 0
    democrat_score = 0

    # Check hashtags
    for tag in republican_tags:
        if f'#{tag}' in tweet_lower or tag in tweet_lower:
            republican_score += 2  # Strong signal

    for tag in democrat_tags:
        if f'#{tag}' in tweet_lower or tag in tweet_lower:
            democrat_score += 2  # Strong signal

    # Check negative words (attacking Biden = Republican)
    for word in negative_words:
        if word in tweet_lower:
            republican_score += 1

    # Check positive words (supporting Biden = Democrat)
    for word in positive_words:
        if word in tweet_lower:
            democrat_score += 1

    # Determine faction
    if republican_score > democrat_score and republican_score > 0:
        return 'Republican', republican_score, democrat_score
    elif democrat_score > republican_score and democrat_score > 0:
        return 'Democrat', republican_score, democrat_score
    else:
        return 'Unclassified', republican_score, democrat_score


# Classify all tweets
results = []
for idx, row in file.iterrows():
    tweet = row.iloc[2]  # Column C (index 2)
    user_id = row.iloc[6]  # Column G (index 6)

    faction, rep_score, dem_score = classify_tweet(tweet)

    results.append({
        'user_id': user_id,
        'tweet': tweet,
        'faction': faction,
        'republican_score': rep_score,
        'democrat_score': dem_score
    })

    print(f"User {user_id}: {faction} (R:{rep_score} D:{dem_score})")

# Create results dataframe
results_df = pd.DataFrame(results)

# Calculate user-level scores
user_scores = results_df.groupby('user_id').agg({
    'republican_score': 'sum',
    'democrat_score': 'sum'
}).reset_index()

user_scores['total_score'] = user_scores['republican_score'] + user_scores['democrat_score']
user_scores['republican_pct'] = (user_scores['republican_score'] / user_scores['total_score'] * 100).fillna(0)
user_scores['democrat_pct'] = (user_scores['democrat_score'] / user_scores['total_score'] * 100).fillna(0)

# Save results
results_df.to_csv('/Users/adrian/Desktop/biden_tweets_classified.csv', index=False)
user_scores.to_csv('/Users/adrian/Desktop/biden_user_scores.csv', index=False)

print("\n=== SUMMARY ===")
print(results_df['faction'].value_counts())
print(f"\n✅ Saved: /Users/adrian/Desktop/biden_tweets_classified.csv and /Users/adrian/Desktop/biden_user_scores.csv")