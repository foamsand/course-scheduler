// Display for a semester and it's courses
import * as React from "react";
import {Semester, ISemester} from "../scripts/Semester"
import CourseView from "./courseView"
import {Course} from "../scripts/Course"

class SemesterView extends React.Component<any, any> 
{
	constructor(props: Semester) 
	{
    super(props);
		// console.log("Semester View 1");
		// console.log(this.props.aSemester);
		this.state = {aSemester: this.props.aSemester};		
		// console.log("Semester View 2");
		// console.log(this.state.aSemester);
		
  }

  render() 
	{
		let courserList: Course[] = this.state.aSemester.theCourses.map(function(aCourse)
		{				
			return <CourseView aCourse={aCourse}/>;
		});

		return(		
			<div>
				<p>Year: {this.state.aSemester.theYear}</p>
				<p>Season: {this.state.aSemester.theSeason}</p>
				<p>Credits: {this.state.aSemester.theCredits}</p>
				<p>Courses: </p>
				<ul>
					{courserList}
				</ul>
			</div>
		);

  }
}

export default SemesterView;