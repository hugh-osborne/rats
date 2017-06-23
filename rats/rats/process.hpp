#pragma once

#include "path.hpp"
#include "placefield.hpp"

class Process {
private:
	GLuint FramebufferName;
	GLuint renderedTexture;

public:
	void init(const char * inputfilename);
	void processInput(int argc, char** argv);
	void writeRenderTexture(const char *filename);
};
