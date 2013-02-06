///////////////////////////////////////////////////////////////////////////////
/// @file   client-structures.h
///
/// @author Ben
///
/// @brief  Client class definitions
///////////////////////////////////////////////////////////////////////////////

#ifndef _CLIENT_STRUCTURES_H_
#define _CLIENT_STRUCTURES_H_

#include <string>

using std::string;

const bool me = true;
const bool enemy = false;

///////////////////////////////////////////////////////////////////////////////
/// @struct coordinate
///
/// @brief Encapsulates a coordinate and implements basic coordinate math
///////////////////////////////////////////////////////////////////////////////
struct coordinate
{
    int x;
    int y;
    
    coordinate();
    coordinate(const int& X, const int& Y);
    coordinate(const coordinate& right);
    coordinate& operator=(const coordinate& right);
    
    bool operator==(const coordinate& right);
    coordinate operator+(const coordinate& right) const;
    coordinate operator-(const coordinate& right) const;
    coordinate operator-() const;
    
    unsigned int distanceTo(const coordinate& calcTo) const;
};


///////////////////////////////////////////////////////////////////////////////
/// @class resource
///
/// @brief Encapsulates a resource node in the game
///////////////////////////////////////////////////////////////////////////////
class resource
{
    public:
        resource();
        resource(const unsigned long& Remaining, const coordinate& Location, const float& MyMultiplier, const float& EnemyMultiplier);
        resource(const resource& right);
        resource& operator=(const resource& right);
        
        
        //Get
        coordinate getLocation() const;
        long getRemaining() const;
        float getMultiplier(bool team = me) const;

        //Set
        void setMultiplier(const float& newMult, bool owner = me);
        void setLocation(const coordinate& newLoc);
        void setRemaining(const long& newRemaining);
    
    private:
        long remaining;
        coordinate location; 
        float myMultiplier;
        float enemyMultiplier;
};


///////////////////////////////////////////////////////////////////////////////
/// @class base
///
/// @brief Encapsulates a base in the game
///////////////////////////////////////////////////////////////////////////////
class base
{
    public:
        
        base();
        base(const bool& Owner, const coordinate& Location);
        base(const base& right);
        base& operator=(const base& right);
        
        //Get
        bool getOwner() const;
        coordinate getLocation() const;
    
        //Set
        void setOwner(const bool& newOwner);
        void setLocation(const coordinate& newLoc);
        
    private:
        coordinate location;
        bool owner;
};


///////////////////////////////////////////////////////////////////////////////
/// @class unitInfo
///
/// @brief Contains all static information about a unit... 
///////////////////////////////////////////////////////////////////////////////
class unitInfo
{
    public:
        
        unitInfo();
        unitInfo(int UnitType, string Name, unsigned long Cost, unsigned long MaxHealth, int AttackPower, int Speed, int AttackRange);
        unitInfo(const unitInfo& right);
        unitInfo& operator=(const unitInfo& right);
        
        bool operator==(const unitInfo& right);
        
        
        //Get
        int getUnitType() const;
        unsigned long getMaxHealth() const;
        int getAttackPower() const;
        int getSpeed() const;
        int getAttackRange() const;
        unsigned long getCost() const;
        string getName() const;
        
        
        //Set
        void setUnitType(const int& newType);
        void setMaxHealth(const unsigned long& newMax);
        void setAttackPower(const int& newPower);
        void setSpeed(const int& newSpeed);
        void setAttackRange(const int& newRange);
        void setCost(const unsigned long& newCost);
        void setName(const string& newName);
        
    private:
        int unitType;
        unsigned long maxHealth;
        int attackPower;
        int speed;
        int attackRange;
        unsigned long cost;
        string name;
};


///////////////////////////////////////////////////////////////////////////////
/// @class unit
///
/// @brief Encapsulates a unit within the game 
///////////////////////////////////////////////////////////////////////////////
class unit
{
    public:
        //Should we write helper functions to access this directly instead of making them do constants->blah?
        unitInfo* constants;
        
        unit();
        unit(int UnitID, unsigned long CurHealth, const coordinate& Location, unitInfo* Constants);
        unit(const unit& right);
        unit& operator=(const unit& right);
        bool operator==(const unit& right);
        
        
        //Get
        int getID() const;
        long getHealth() const;
        coordinate getLocation() const;
        unsigned int distanceTo(const coordinate& calcTo) const;
        int getMoves() const;
        
        //Set
        void setID(const int& newID);
        void setHealth(const long& newHealth);
        void setLocation(const coordinate& newLoc);
        void setMoves(int newMoves);
    
    
    private:
        int unitID;
        long curHealth;
        coordinate location;
        int moves;
};

///////////////////////////////////////////////////////////////////////////////
/// @class order
///
/// @brief Encapsulates an order
///////////////////////////////////////////////////////////////////////////////
class order
{
   public:
      string s_expression;
};


#endif
