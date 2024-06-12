#include <iostream>

const long LOOPS = 100'000'000;

char tossCoin() {
    if (std::rand() % 2 + 1 == 1)
        return 'H'; // Head
    else
        return 'T'; // Tail
}

// Players
class Player {
    public:
    int wins = 0;
    virtual std::string name() = 0;
    virtual char predict(long heads, long tails) = 0;
};

class CasualPlayer: public Player {
    public:
    std::string name() override {
        return "Casual";
    }
    
    char predict(long heads, long tails) override {
        if (heads == tails)
            return tossCoin();
        else if (heads < tails)
            return 'H';
        else
            return 'T';
    }
};

class RandomPlayer: public Player {
    public:
    std::string name() override {
        return "Random";
    }

    char predict(long heads, long tails) override {
        return tossCoin();
    }
};

// Players list
Player *players[2] = {
    new CasualPlayer(),
    new RandomPlayer(),
};

int main() {
    std::srand(std::time(nullptr));  // Init rand

    long heads = 0;
    long tails = 0;

    char winner;
    for (long i = 0; i < LOOPS; i++) {
        winner = tossCoin();

        for (Player *player: players) {
            if (player->predict(heads, tails) == winner)
                player->wins++;
        }

        if (winner == 'H')
            heads++;
        else
            tails++;
    }

    std::cout << "Results:" << std::endl;
    for (Player *player: players) {
        std::cout << 
        "Player: " << player->name() << ", " <<
        "wins: " << player->wins << ", " <<
        "winrate: " << (double) player->wins / LOOPS << std::endl;
    }

    std::cout << std::endl << "Coins" << std::endl;
    std::cout << "heads: " << heads << std::endl;
    std::cout << "tails: " << tails << std::endl;
}
