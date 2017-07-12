#include <stdio.h>
#include <stdlib.h>
#include "../include/glm/glm.hpp"
#include "defs.hpp"

class PathPoint {
public:
	glm::vec2 position;
	GLfloat time;

	PathPoint(glm::vec2 _position, GLfloat _time) :
		position(_position),
		time(_time){ }
};
