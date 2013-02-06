///////////////////////////////////////////////////////////////////////////////
/// @file   shellAI.cpp
///
/// @author Ben
///
/// @brief  Shell API implementation file for competitors to fill out
///////////////////////////////////////////////////////////////////////////////

#include "shellAI.h"

//Initialization
myAI::myAI() : baseAI()
{
	

}

//Cleanup
myAI::~myAI()
{
	

}

//Play function, called at the start of every turn
void myAI::Play()
{
	static int nextUnit = 3;
	static int unit1 = 3;
	static int unit2 = 0;


	long money;
	money = myScore;

	
	cout << "Play is called.  Turn = " << turnNumber << " Units: " << myUnits.size() << endl;
	
	if (myScore > enemyScore && enemyUnits.size() == 0 && enemyScore < 15)
	{
		//Rock the party
	}
	else
	{

		MoveAllUnits();


	
		while (money >= unitTypes[nextUnit].getCost() && (myUnits.size() <= enemyUnits.size() * 10 + 20))
		{
			BuyUnit(&unitTypes[nextUnit]);
			money -= unitTypes[nextUnit].getCost();
			
			if (nextUnit == unit1)
			{
				nextUnit = unit2;
			}
			else
			{
				nextUnit = unit1;
			}
		}
	}


   return;
}



//Return your name
string myAI::PlayerName()
{
   return string("Stephen's AI");
}

void myAI::MoveAllUnits()
{
	for (int i = 0; i < myUnits.size(); i++)
	{
		if (i < myUnits.size())
			MoveUnit(myUnits[i]);
	}

}

void myAI::DoMove(unit& person, Order& myOrder)
{
	switch(myOrder.type)
	{
	case 0:		//Move
		//cout << "Moving Target (" << myOrder.target.x << ", " << myOrder.target.y << ")";
		if ( !(person.getLocation() == myOrder.target) )
		{
			Move(person, myOrder.target);
		}
		break;
	case 1:		//Attack
		if (person.constants->getUnitType() == 3)
		{
			cout << person.getID() << " is Attacking Target (" << myOrder.target.x << ", " << myOrder.target.y << ")" << endl;
			person.setMoves(0);
		}

		Attack(person, myOrder.target);
		break;
	case 2:		//Gather
		//cout << "Gathering Target (" << myOrder.target.x << ", " << myOrder.target.y << ")";
		Gather(person, myOrder.target);
		break;
	}
}


Order myAI::BestMove(unit& person, coordinate location, int turns)
{
	const int TARGET_SIZE = 76;

	static float PERSONAL_SPACE = 0.1;


	Order myBestMove;
	float tempMoveScore;
	coordinate target[TARGET_SIZE];
	coordinate nextCoord;

	bool isValidMoveTarget[9];
	bool isValidGatherTarget[9];
	bool isValidHealTarget[9];
	bool isValidAttackTarget[TARGET_SIZE];

	int index;

	myBestMove.value = -99999999;
	myBestMove.type = 0;
	myBestMove.target = location;
	
	target[0] = location + coordinate(-1, 1);
	target[1] = location + coordinate(0, 1);
	target[2] = location + coordinate(1, 1);
	target[3] = location + coordinate(-1, 0);
	target[5] = location + coordinate(0, 0);
	target[4] = location + coordinate(1, 0);
	target[6] = location + coordinate(-1, -1);
	target[7] = location + coordinate(0, -1);
	target[8] = location + coordinate(1, -1);
	
	/*	
	int threat = 0;
	coordinate worstEnemy = center;
	
	for( int a = 0; a < enemyUnits.size(); a++)
	{
		if(UnitThreat(myUnits[i], enemyUnits[a]) > threat)
		{
			threat = UnitThreat(myUnits[i], enemyUnits[a]);
			worstEnemy = enemyUnits[a];
		}
	}
	*/

	index = 9;
	for (int row = 0; row < 7; row++)
	{
		for (int col = -row; col <= row; col++)
		{
			nextCoord = location + coordinate( col, 6 - row);
			if ((col > 1 || col < -1 || row < 5) && index < TARGET_SIZE)
			{
				target[index] = nextCoord;
				index++;
			}

			if (row < 6)
			{
				nextCoord = location + coordinate( col, -6 + row);
				if ((col > 1 || col < -1 || row < 5) && index < TARGET_SIZE)
				{
					target[index] = nextCoord;
					index++;
				}
			}
		}
		
	}
	

	//validate Targets
	for (int i = 0; i < TARGET_SIZE; i++)
	{
		isValidAttackTarget[i] = false;
		if (i < 9)
		{
			isValidHealTarget[i] = false;
			isValidMoveTarget[i] = true;
			isValidGatherTarget[i] = false;

			//bases prevent movement
			if (enemyBase == target[i])
			{
				isValidMoveTarget[i] = false;
			}
				
			//nodes prevent movement and allow gathering
			for (int j = 0; j < resourceNodes.size(); j++)
			{
				if (resourceNodes[j].getLocation() == target[i])
				{
					if (resourceNodes[j].getRemaining() > 0)
					{
						isValidGatherTarget[i] = true;
						isValidMoveTarget[i] = false;
					}
				}
			}
	

			//friendlys allow heal
			for (int j = 0; j < myUnits.size(); j++)
			{
				if (myUnits[j].getLocation() == target[i])
				{
					isValidHealTarget[i] = true;
				}
			}
			

		}


		//enemies prevent movement, allow attack
		for (int j = 0; j < enemyUnits.size(); j++)
		{
			if (enemyUnits[j].getLocation() == target[i] && enemyUnits[j].getHealth() > 0)
			{
				if (i < 9)
				{
					isValidMoveTarget[i] = false;
				}
				isValidAttackTarget[i] = true;
			}
		}

		//Borders prevent movement and gathering and attacking
		if (target[i].x < MIN_COORD 
			|| target[i].x > MAX_COORD
			|| target[i].y < MIN_COORD
			|| target[i].y > MAX_COORD)
		{
			if (i < 9)
			{
				isValidMoveTarget[i] = false;
				isValidGatherTarget[i] = false;
			}
			isValidAttackTarget[i] = false;
		}
	}
	

	//Consider move options
	for (int i = 0; i < 9; i++)
	{
		
		if (isValidMoveTarget[i])
		{

			tempMoveScore = 0;
			if (turns == 1)
			{
				tempMoveScore = 0 - ResourceDistance(target[i])/10.0;
				//Poof!
				tempMoveScore -= 1 * (ThreatLevel(location) + PERSONAL_SPACE) * CountFriendliesInZone(target[i]);
			}
			else
			{
				tempMoveScore = (BestMove(person, target[i], turns - 1)).value;
			}

			if (tempMoveScore > myBestMove.value)
			{
				myBestMove.value = tempMoveScore;
				myBestMove.type = 0;
				myBestMove.target = target[i];
			}
		}
	}

	//consider gather options
	for (int i = 0; i < 9; i++)
	{
		if (isValidGatherTarget[i])
		{
			tempMoveScore = 0;
			float gatherValue = GetResourceAtZone(target[i]).getMultiplier();
			if (turns == 1)
			{
				tempMoveScore = 0 - ResourceDistance(location)/10.0;
				tempMoveScore += gatherValue;
				//Double poof?
				tempMoveScore -= 1 * (ThreatLevel(location) + PERSONAL_SPACE) * CountFriendliesInZone(location);
			}
			else
			{
				tempMoveScore = gatherValue;
				tempMoveScore += BestMove(person, location, turns - 1).value;
			}

			if (tempMoveScore > myBestMove.value)
			{
				myBestMove.value = tempMoveScore;
				myBestMove.type = 2;
				myBestMove.target = target[i];
			}
		}
	}


	switch (person.constants->getUnitType())
	{
	case 0:	//Fighter
		for (int i = 0; i < 9; i++)
		{
			if (isValidAttackTarget[i])
			{
				tempMoveScore = 0;
				if (turns == 1)
				{
					tempMoveScore -= ResourceDistance(location)/10.0;
				}
				else
				{
					tempMoveScore += BestMove(person, location, turns - 1).value;
				}

				tempMoveScore += 1.5 *( person.constants->getAttackPower() * CountEnemiesInZone(target[i]));

				
				//cout << tempMoveScore  << " to " << myBestMove.value << " for " << myBestMove.type << endl;
				if (tempMoveScore > myBestMove.value)
				{
					myBestMove.value = tempMoveScore;
					myBestMove.type = 1;
					myBestMove.target = target[i];
				}	
			}
		}
		break;

	case 1:	//Medic

		//myBestMove = HealingValue(person, myBestMove);

		for (int i = 0; i < 9; i++)
		{
			if (isValidHealTarget[i])
			{
				tempMoveScore = 0;
				if (turns == 1)
				{
					tempMoveScore -= ResourceDistance(location)/10.0;
					tempMoveScore -= (ThreatLevel(location) + PERSONAL_SPACE) * CountFriendliesInZone(location);
				}
				else
				{
					tempMoveScore += BestMove(person, location, turns - 1).value;
				}
				tempMoveScore += (person.constants->getAttackPower() * CountFriendliesInZone(target[i]));
								
				if (myBestMove.value < tempMoveScore)
				{
					myBestMove.value = tempMoveScore;
					myBestMove.type = 1;
					myBestMove.target = target[i];
				}	
			}
		}
		break;

	case 2:	//Sniper
		for (int i = 0; i < TARGET_SIZE; i++)
		{
			if (isValidAttackTarget[i])
			{
				tempMoveScore = 0;
				if (turns == 1)
				{
					tempMoveScore -= ResourceDistance(location)/10.0;
					tempMoveScore -= 1.5 * (ThreatLevel(location) + PERSONAL_SPACE) * CountFriendliesInZone(location);
				}
				else
				{
					tempMoveScore += BestMove(person, location, turns - 1).value;
				}
				tempMoveScore += 2 * (person.constants->getAttackPower() * CountEnemiesInZone(target[i]));
								
				if (myBestMove.value < tempMoveScore)
				{
					myBestMove.value = tempMoveScore;
					myBestMove.type = 1;
					myBestMove.target = target[i];
				}	
			}
		}
		break;

	case 3:	//Bomber!

		//consider explosion
		tempMoveScore = ExplosionValue(location);
		//if (myBestMove.value < tempMoveScore)
		if (tempMoveScore > myBestMove.value)
		{
			//cout << "Explosion to (" << location.x << ", " << location.y << ") = " << tempMoveScore << endl;
			myBestMove.value = tempMoveScore;
			myBestMove.type = 1;
			myBestMove.target = location;
		}	
		break;
	}
	
	return myBestMove;
}


/*
for( int a = 0; a < enemyUnits.size(); a++)
{
	if(UnitThreat(player, enemyUnits[a]) > threat)
		threat = UnitThreat(player, enemyUnits[a]);
}
*/

resource myAI::GetResourceAtZone(coordinate& zone)
{
	resource retVal;
	for (int i = 0; i < resourceNodes.size(); i++)
	{
		if (resourceNodes[i].getLocation() == zone)
		{
			retVal = resourceNodes[i];
		}
	}

	return retVal;
}

int myAI::CountFriendliesInZone(coordinate& zone)
{
	int count = 0;
	for (int i = 0; i < myUnits.size(); i++)
	{
		if (myUnits[i].getLocation() == zone  && myUnits[i].getHealth() > 0)
		{
			count += 1;
		}
	}

	return count;
}

int myAI::CountEnemiesInZone(coordinate& zone)
{
	int count = 0;
	for (int i = 0; i < enemyUnits.size(); i++)
	{
		if (enemyUnits[i].getLocation() == zone && enemyUnits[i].getHealth() > 0)
		{
			count += 1;
		}
	}

	return count;
}



void myAI::MoveUnit(unit& person)
{
	Order myBestMove;
	int turnsLeft = person.getMoves();
	
	while (turnsLeft > 0)
	{
		//cout << turnsLeft << endl;
		myBestMove = BestMove(person, person.getLocation(), turnsLeft);
		DoMove(person, myBestMove);
		turnsLeft = min(turnsLeft - 1, person.getMoves());
	}
}


int myAI::ThreatLevel(coordinate& zone)
{
	int effectiveRange = 0;
	int threat = 0;

	for (int i = 0; i< enemyUnits.size(); i++)
	{
		effectiveRange = 0;
		effectiveRange += enemyUnits[i].constants->getSpeed() - 1;
		effectiveRange += enemyUnits[i].constants->getAttackRange();
		if (enemyUnits[i].constants->getUnitType() == BOMBER_TYPE)
		{
			effectiveRange += SPLASH_RANGE;
		}


		if (enemyUnits[i].distanceTo(zone) <=  effectiveRange)
		{
			threat += enemyUnits[i].constants->getAttackPower();
		}
	}

	return threat;
}


int myAI::ExplosionValue(coordinate& zone)
{
	int damageValue = -unitTypes[BOMBER_TYPE].getCost();
	int damageDelt;
	
	for (int i = 0; i< enemyUnits.size(); i++)
	{
		if (enemyUnits[i].distanceTo(zone) <= SPLASH_RANGE && enemyUnits[i].getHealth() > 0)
		{
			damageDelt = unitTypes[BOMBER_TYPE].getAttackPower();
			damageValue += (damageDelt * enemyUnits[i].constants->getCost() / enemyUnits[i].constants->getMaxHealth());
		}
	}

	return damageValue;
}

coordinate myAI::nearestResource(unit& toFind)
{
    coordinate unitLoc = toFind.getLocation();
    
    coordinate nearest;
    
    int minDist = 100;
    int tempDist = 0;
    
    for(int i=0; i < resourceNodes.size(); i++)
    {
        tempDist = toFind.distanceTo(resourceNodes[i].getLocation());
        if(tempDist <= minDist)
        {
            minDist = tempDist;
            nearest = resourceNodes[i].getLocation();
        }
    }



    return nearest;
}

int myAI::ResourceDistance(coordinate& zone)
{
    int minDist = 100;
    int tempDist;
    
    for(int i=0; i < resourceNodes.size(); i++)
    {
		if (resourceNodes[i].getRemaining() > 0 )
		{
			tempDist = zone.distanceTo(resourceNodes[i].getLocation());
			if(tempDist <= minDist)
			{
	            minDist = tempDist;
			}
		}
    }
    return minDist;
}

void myAI::moveToward(unit& toMove, const coordinate& moveTo)
{
    coordinate curLoc = toMove.getLocation();
    coordinate desired = curLoc - moveTo;
    
    if(desired.x > 0)
        desired.x = min(desired.x, 1);
    else
        desired.x = -min(-desired.x,1);

    if(desired.y > 0)
        desired.y = min(desired.y, 1);
    else
        desired.y = -min(-desired.y,1);
    
    curLoc = curLoc - desired;
    
    Move(toMove, curLoc);
}


Order myAI::HealingValue(unit& medic, Order& Best)
{
  Best.type = 0;
  Best.target = enemyBase;

  int HealValue = 0;
  for(int i = 0; i < myUnits.size(); i++)
  {
    if(((-1 * (medic.getHealth() - medic.constants->getMaxHealth())) - (medic.distanceTo(myUnits[i].getLocation()))) > HealValue)
    {
      Best.target= myUnits[i].getLocation();
      if( medic.distanceTo( myUnits[i].getLocation() ) == 1)
      {
        Best.type = 1;
      }
    }
  }
  if(Best.target == enemyBase)
  {
     Best.type = 2;
     Best.target = nearestResource(medic);
  }
  return  Best;
}


int myAI::UnitThreat(unit& enemy, unit& person)
{
  int effectiveRange = 0;
  int threat = 0;
  for (int i = 0; i< enemyUnits.size(); i++)
  {
    effectiveRange = 0;
    effectiveRange += enemyUnits[i].constants->getSpeed() - 1;
    effectiveRange += enemyUnits[i].constants->getAttackRange();
    if (enemy.constants->getUnitType() == BOMBER_TYPE)
    {
      effectiveRange += SPLASH_RANGE;
    }
    if (person.distanceTo(enemy.getLocation()) <= effectiveRange)
      threat += enemy.constants->getAttackPower();
  }
  return threat;
}

