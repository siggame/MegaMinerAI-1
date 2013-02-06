///////////////////////////////////////////////////////////////////////////////
/// @file   shellAI.h
///
/// @author Ben
///
/// @brief  Shell AI header file for competitors to fill in.
///////////////////////////////////////////////////////////////////////////////
#ifndef _SHELLAI_H_
#define _SHELLAI_H_

#include "../baseAI.h"
#include "../client-structures.h"

///////////////////////////////////////////////////////////////////////////////
/// @class  myAI
///
/// @brief  Shell AI for competitors to fill in.
///
/// @details The competitors will implement the Play() and PlayerName()
///          functions. They will have access to everything defined in baseAI,
///          but should only need access to the items commented out (provided
///          for reference).
///////////////////////////////////////////////////////////////////////////////
class myAI : public baseAI
{
   public:
      
      myAI();
      ~myAI();
      void Play();
      string PlayerName();
   
      long minCost;
      int nextPurchase;
      
      void unitAction(unit* fighter);
      
      void moveToCenter(unit* toMove);
      void moveToward(unit* toMove, const coordinate& moveTo);
      coordinate nearestEnemy(unit* toFind);
      coordinate nearestResource(unit* toFind);
   
      coordinate center;
      //From baseAI
      //vector<unit> myUnits;          //Vector of AI's units on the map
      //vector<unit> enemyUnits;       //Vector of enemy units on the map
      //vector<base> bases;            //Vector of bases on the map
      //vector<resource> resourceNodes;//Vector of resource nodes on the map
      //vector<unitInfo> unitTypes;    //Vector of unit types
      //long myScore;      //Score of the AI
      //long enemyScore;   //Score of the enemy
      //int turnNumber;    //Current turn number
      //int maxTurns;      //The turn number that ends the game
      
      
      //void BuyUnit(unitInfo* typeToBuy);
      //void Move(const unit& toMove, const coordinate& moveTo);
      //void Attack(const unit& attackWith, const coordinate& attackCoord);
      //void Gather(const unit& toGather, const coordinate& attackCoord);
   
};





#endif
