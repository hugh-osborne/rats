#pragma once
#include <vector>
#include <deque>
#include "defs.hpp"
#include "placecell.hpp"

class HMM {
private:
	GLfloat start_time;
	GLfloat bin_size;
	std::vector<std::vector<GLfloat> > spike_obs;
	std::vector<std::vector<GLfloat> > spike_model;

	GLfloat p_infield_to_outfield;
	GLfloat p_outfield_to_infield;
	GLfloat p_infield_spike;
	GLfloat p_outfield_spike;
	GLfloat alpha_infield;
	GLfloat alpha_outfield;

public:

	HMM(PlaceCell *pc, GLfloat start_time, GLfloat end_time);
	std::deque<GLfloat> getSpikeTimes();


};
