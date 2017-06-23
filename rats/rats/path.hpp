#pragma once
#include "pathpoint.hpp"
#include <deque>

class Path {
private:
	std::deque<PathPoint> points;
	std::deque<PathPoint>::iterator current_point;
	GLfloat start_time;
	GLfloat end_time;

public:
	Path();
	Path(const char *pathFilename);
	PathPoint* getNextPoint();

	GLfloat getStartTime();
	GLfloat getEndTime();

	void reset();

};
