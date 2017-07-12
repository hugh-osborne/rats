#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <cstdlib>
#include <string>
#include <sstream>
#include <vector>
#include <iterator>
#include "path.hpp"
//#include <GL/glut.h>
#include "../include/GL/glut.h"
#include "stringsplit.hpp"

Path::Path() {
	
}

Path::Path(const char *filename) {
	std::ifstream input(filename);

	GLfloat max_x = -99999.0f;
	GLfloat min_x = 99999.0f;
	GLfloat max_y = -99999.0f;
	GLfloat min_y = 99999.0f;

	for ( std::string line; std::getline(input, line); ) {
		std::vector<std::string> elems = StringSplit::split(line, ',');
		GLfloat time = std::atof(elems[0].c_str());
		GLfloat posx = std::atof(elems[1].c_str());
		GLfloat posy = std::atof(elems[2].c_str());

		if(posx > max_x) max_x = posx;
		if(posx < min_x) min_x = posx;
		if(posy > max_y) max_y = posy;
		if(posy < min_y) min_y = posy;

		glm::vec2 pos(posx,posy);
		PathPoint p(pos,time);
		points.push_back(p);
	}

	GLfloat width = (max_x - min_x) / 2.0f;
	GLfloat height = (max_y - min_y) / 2.0f;
	GLfloat centre_x = min_x + width;
	GLfloat centre_y = min_y + height;

	std::deque<PathPoint>::iterator it = points.begin();
	while(it != points.end()) {
		(*it).position.x = ((*it).position.x - centre_x ) / width;
		(*it).position.y = ((*it).position.y - centre_y ) / height;
		it++;
	}

	current_point = points.begin();
	start_time = points.front().time;
	end_time = points.back().time;

	input.close();
}

PathPoint *Path::getNextPoint() {
	if(current_point == points.end())
		return 0;

	return &(*(current_point++));
}

GLfloat Path::getStartTime() {
	return start_time;
}

GLfloat Path::getEndTime() {
	return end_time;
}

void Path::reset() {
	current_point = points.begin();
	start_time = points.front().time;
	end_time = points.back().time;
}
