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

#include <algorithm>
#include <iostream>
#include <ctime>
using namespace std;

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


const int BOMBER_TYPE = 3;
const int SPLASH_RANGE = 4;
const int MIN_COORD = 0;
const int MAX_COORD = 25;





struct Order
{
	float value;
	int type;
	// 0 = move
	// 1 = attack
	// 2 = gather
	coordinate target;
};

class myAI : public baseAI
{
   public:
      
      myAI();
      ~myAI();
      void Play();
      string PlayerName();
	  void MoveAllUnits();
	  void MoveUnit();
	  void MoveUnit(unit& person);

	  coordinate nearestResource(unit& toFind);

	  int ThreatLevel(coordinate& zone);
	  int ExplosionValue(coordinate& zone);
	  int ResourceDistance(coordinate& zone);
	  resource GetResourceAtZone(coordinate& zone);

	  int CountFriendliesInZone(coordinate& zone);
	  Order BestMove(unit& person, coordinate location, int turns);
	  void MoveBomber(unit& person);

		void moveToward(unit& toMove, const coordinate& moveTo);

		void DoMove(unit& person, Order& myOrder);

		int CountEnemiesInZone(coordinate& zone);

		Order HealingValue(unit& medic, Order& Best);

	int UnitThreat(unit& enemy, unit& person);

		   
      //From baseAI
      //vector<unit> myUnits;          //Vector of AI's units on the map
      //vector<unit> enemyUnits;       //Vector of enemy units on the map
      //vector<resource> resourceNodes;//Vector of resource nodes on the map
      //vector<unitInfo> unitTypes;    //Vector of unit types
      
      //long myScore;      //Score of the AI
      //long enemyScore;   //Score of the enemy
      //coordinate myBase; //Location of your base
      //coordinate enemyBase; //Location of the enemy base
      
      //int turnNumber;    //Current turn number
      //int maxTurns;      //The turn number that ends the game
      
      
      //void BuyUnit(unitInfo* typeToBuy);
      //void Move(const unit& toMove, const coordinate& moveTo);
      //void Attack(const unit& attackWith, const coordinate& attackCoord);
      //void Gather(const unit& toGather, const coordinate& gatherCoord);
   
};





#endif
