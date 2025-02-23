#include "pch.h"
#include "CppUnitTest.h"
#include "C:\Users\user\source\repos\TimeTest\Source.cpp"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTest5
{
	TEST_CLASS(UnitTest5)
	{
	public:
		
			set<int> set;
			TEST_METHOD(a_lot_of_nums)
			{
				Assert::IsTrue(pow(10, 7) >= Set_time_measure(set, 1000000));
			}
			TEST_METHOD(average_nums)
			{
				Assert::IsTrue(pow(10, 5) >= Set_time_measure(set, 100000));
			}
			TEST_METHOD(little_nums)
			{
				Assert::IsTrue(pow(10, 3) >= Set_time_measure(set, 1000));
			}
		
	};
}
