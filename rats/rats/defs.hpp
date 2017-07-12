#define LINUX
//#define WIN

#ifdef WIN
#include "../include/GL/glew.h"
#include "../include/GL/glut.h"
#endif
#ifdef LINUX
#include "../include/GL/glew.h"
#include <GL/glut.h>
#endif
