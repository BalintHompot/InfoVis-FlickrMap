
        function getStreamData(country_key, timeSteps, level){
            //updatedMultiDonut(country_key, timeSteps);

            var d = []
            var keys = new Set()
            var maxYear = 0

            if(level == "tag"){
                reverseTagCatIndex = {}
                allTagsEmpyty = {}
                for(var timeStepInd in timeSteps){
                    var timeStep = timeSteps[timeStepInd]
                    var country_bucket = countries_mock_data.timesteps[timeStep].country_data.buckets.find( function (e){
                        return e.key == country_key
                    })
                    if(country_bucket){
                        var catList = Object.keys(country_bucket.categories)
                        for(catInd in catList){
                        var catObj = country_bucket.categories[catList[catInd]]
                
                        if(catObj){
                            catTags = Object.keys(catObj.top_5)
                            for(catTagInd in catTags){
                                allTagsEmpyty[catTags[catTagInd]] = 0
                                
                                reverseTagCatIndex[catTags[catTagInd]] = catList[catInd]
                        
                            
                        }
                        }
                        reverseTagCatIndex["other " + catList[catInd] + " tags"] = catList[catInd]
                    }
                    }

                    
                }
            
            }

            var tags
            var year_count = 0
            for(var timeStepInd in timeSteps){
                year_count = 0
                var timeStep = timeSteps[timeStepInd]
                var country_bucket = countries_mock_data.timesteps[timeStep].country_data.buckets.find( function (e){
                    return e.key == country_key
                })
                emptyObj = level == "tag"?allTagsEmpyty:allCategoriesEmpyty

                var year_data = {"time_step_graph" : timeStep}
                Object.assign(year_data, emptyObj);
                if(country_bucket){
        
                    //var tags = Object.assign({}, country_bucket.most_popular_5, country_bucket.rest_tags)
                    tags = JSON.parse(JSON.stringify(country_bucket.categories_tags_sum))
            
                    tag_list = Object.keys(tags)

                
                        
                        if(level == "category" && filterString == null){
                            for(var tagInd in tag_list){
                                tag = tag_list[tagInd]
                                year_count += tags[tag]
                                year_data[tag] = tags[tag]
                                keys.add(tag)
                            }
                        }else{
                        
                            var allTagsList = {}
                            for(var tagInd in tag_list){
                                cat = tag_list[tagInd]
                                cat_obj = country_bucket.categories[cat]
                                if(cat_obj){
                                    all_cat_tag_obj = cat_obj.all_tags
                                    allTagsList = Object.assign(allTagsList, all_cat_tag_obj)
                                }
                            
                            }
                            var catTagList =Object.keys(emptyObj)
                            if(filterString!=null){
                                catTagList = [filterString]
                            }
                
                            for(var catInd in catTagList){

                    
                                var catCount =  allTagsList[catTagList[catInd]]
                                
                                if(typeof catCount == "undefined"){
                                    catCount = 0
                                }
                                
                                if(level == "tag"){
                                    year_data[catTagList[catInd]] = catCount
                                    keys.add(catTagList[catInd])
                                }else{
                        
                                    year_data[filterCategory] = catCount
                                    keys.add(filterCategory)
                                }
                                
                                year_count += catCount
                            
                            }
                                
                    
    
                        /*
                        // pushing untagged data into focused
                        for(var c in Object.keys(tags)){
                            var cat_untagged = Object.keys(tags)[c]
                            var other_tag = "other " + cat_untagged + " tags"
                            year_data[other_tag] = tags[cat_untagged]
                            keys.add(other_tag)
                            year_count += tags[cat_untagged]

                        }
                        */
                        
                    }
                }
            
                d.push(year_data)
                if (year_count>maxYear){
                    maxYear = year_count
                }
        

            }
            keys = Array.from(keys)


            return [d, maxYear, keys]
        }
    
    function getX(validTimeSteps_x, width_stream_x){
        var x = d3.scaleOrdinal()
        var stramChartXRange = []
        var rangeStep = width_stream_x / validTimeSteps_x.length
        step = 0
        for(t in validTimeSteps_x){
            stramChartXRange.push(step)
            step += rangeStep
        }

        // Add X axis
        x
            .domain(validTimeSteps_x)
            .range(stramChartXRange);
        return x
    }

    function getY(maxRange, height_stream_y){
        var y = d3.scaleLinear()
        y
            .domain([0, maxRange ])
            .range([ height_stream_y * 0.8, 20 ]);
        return y

    }
    
    
    function getFocusedValidSteps(){
        var start_index = Math.max(current_date_ind - rectWidthLeftSteps, 0)
        var end_index = Math.min(current_date_ind + rectWidthRightSteps, validTimeSteps.length)
        timesteps = []
        for(start_index; start_index<=end_index; start_index++){
            timesteps.push(validTimeSteps[start_index])
        }
        return timesteps
    }

    function invertX(xpos){
        var ypos = x_main_stream.domain()[d3.bisect(x_main_stream.range(), xpos) - 1];
        return ypos
    }

    function dragged(d) {
        /*
        console.log("d x is")
        console.log(d.x)
        console.log("mouse pos x")
        console.log(d3.event.x )
        */
        sliderGPosX = d3.event.x - width_side_panel
        d3.selectAll("#sliderG")
        .data([{x: sliderGPosX, y: 0}]);

        current_date = invertX(d3.event.x  - width_side_panel) 
        current_date_ind = validTimeSteps.findIndex((element) => element == current_date)
        updateStreamSlider()
    }

    function draggedLeft(d) {
        current_time_pos = x_main_stream(current_date)
        current_mouse_pos = d3.event.x - rectWidthLeft - width_side_panel
        time_step_size = (width_stream / validTimeSteps.length)
        if(current_time_pos - current_mouse_pos > time_step_size * (rectWidthLeftSteps+1)){
            rectWidthLeftSteps = Math.min(rectWidthLeftSteps+1, current_date_ind )

            rectWidthLeft = time_step_size * rectWidthLeftSteps
            updateStreamSlider()
        }else if(current_time_pos - current_mouse_pos < time_step_size * (rectWidthLeftSteps-1)){
            rectWidthLeftSteps = Math.max(1, rectWidthLeftSteps-1)
            rectWidthLeft = time_step_size * rectWidthLeftSteps
            updateStreamSlider()
        }
    }

    function draggedRight(d) {
        current_time_pos = x_main_stream(current_date)
        current_mouse_pos = d3.event.x + rectWidthRight - width_side_panel
        time_step_size = (width_stream / validTimeSteps.length)
        if(current_mouse_pos - current_time_pos > time_step_size * (rectWidthRightSteps+1)){
            rectWidthRightSteps = Math.min(rectWidthRightSteps+1, validTimeSteps.length - current_date_ind - 1)
            rectWidthRight = time_step_size * rectWidthRightSteps
            updateStreamSlider()
        }else if(current_mouse_pos - current_time_pos < time_step_size * (rectWidthRightSteps-1)){
            rectWidthRightSteps = Math.max(1, rectWidthRightSteps-1)
            rectWidthRight = time_step_size * rectWidthRightSteps
            updateStreamSlider()
        }
    }



    function drawStreamGraph(country_key, svg_stream, validTimeSteps_graph, width_stream_graph, height_stream_graph, level, ticksEnabled = true){
// append the svg object to the body of the page

        //svg_stream.selectAll("path").remove()
        console.log("valid ts: ",validTimeSteps_graph);

        // Parse the Data
        var [data, yRange, keys] = getStreamData(country_key, validTimeSteps_graph, level)

        var x = getX(validTimeSteps_graph, width_stream_graph)
        var y = getY(yRange, height_stream_graph-5)

            svg_stream.append("g")
            .attr("transform", "translate(0," + height_stream_graph*0.8 + ")")
            .call(d3.axisBottom(x).tickSize(-height_stream_graph*.7)
			.tickValues(validTimeSteps_graph)
			.tickFormat(function(d, i){
                if(ticksEnabled){
                    var year = d.substring(0,4);
				    if (!(i % 4)) return year;
                }else{
                    return ""
                }
		
			})
			)
            .select(".domain").remove()
        // Customization

        svg_stream.selectAll(".tick line")
        .attr("stroke", "grey")
        if(level == "category"){
            svg_stream.selectAll(".tick line")
            .attr("stroke-opacity", 0.8);
        }


			
		svg_stream_2.selectAll(".tick line")
        .attr("stroke", "grey")
        if(level == "category"){
            svg_stream.selectAll(".tick line")
            .attr("stroke-opacity", 0.8);
        }
		
		if(ticksEnabled){
            // Add X axis label:
            svg_stream_2.append("text")
                .attr("text-anchor", "end")
                .attr("x", width_stream_graph)
                .attr("y", height_stream_graph -3 )
                .attr('font-size', 12)
                .text("Year");
        }
		



        // Add Y axis

        //stack the data?
        var stackedData = d3.stack()
            //.offset(d3.stackOffsetSilhouette)
            .keys(keys)
            (data)


        // create a tooltip
        var Tooltip = svg_stream
            .append("text")
            .attr("id", "stream-tooltip")
            .attr("x", 0)
            .attr("y", 20)
            .style("opacity", 0)
            .style("font-size", 17)

        // Three function that change the tooltip when user hover / move / leave a cell
        var mouseover = function(d) {
            Tooltip.style("opacity", 1)
            d3.selectAll(".myArea-" + level ).style("opacity", .2)
            d3.select(this)
            .style("stroke", "black")
            .style("opacity", 1)
        }
        var mousemove = function(d,i) {
            grp = d.key
            Tooltip.text(grp)
 
        }
        var mouseleave = function(d) {
            Tooltip.style("opacity", 0)
            d3.selectAll(".myArea-" + level ).style("opacity", 1)
            d3.selectAll(".myArea-category" ).style("stroke", "none")
        }

        var clickedStream = function(d){

            current_date = invertX(d3.mouse(this)[0])
            current_date_ind = validTimeSteps_graph.findIndex((element) => element == current_date)
            updateStreamSlider()
        }


        var clickedStreamFocused = function(d){
            document.getElementById("filterInput").value = d.key
            filterTagsByString()
            
        }

        var clickFunction = level == "category"?clickedStream:clickedStreamFocused


        var logged = false
        // Area generator
        var area = d3.area()
            .x(function(d) {return x(d.data.time_step_graph); })
            .y0(function(d) {return y(d[0]); })
            .y1(function(d) { return y(d[1]); })
        

        // Show the areas
        svg_stream
            .selectAll("mylayers")
            .data(stackedData)
            .enter()

            .append("path")
            .attr("id", function(d){return "path-" + d.key})
            
            .attr("class", "myArea-" + level )
            .style("fill", function(d) {                     
           
                    if(!d){
                    return 'grey'
                    }else if(level == "tag"){
                        return myColor(reverseTagCatIndex[d.key]) 
                    }else{
                        return myColor(d.key)
                    } })
            .attr("d", area)
            
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave)
            .on("click", clickFunction);


    }

    function refreshStreamGraph(country_key, svg_stream, validTimeSteps_graph, width_stream_graph, height_stream_graph, level, ticksEnabled = true){
        svg_stream.selectAll(".tick").remove()

        // Parse the Data


        var [data, yRange, keys] = getStreamData(country_key, validTimeSteps_graph, level)


        var x = getX(validTimeSteps_graph, width_stream_graph)
        var y = getY(yRange, height_stream_graph)

        // List of groups = header of the csv files
        svg_stream.append("g")
            .attr("transform", "translate(0," + height_stream_graph*0.8 + ")")
            .call(d3.axisBottom(x).tickSize(-height_stream_graph*.7)
			.tickValues(validTimeSteps_graph)
			.tickFormat(function(d, i){
                if(ticksEnabled){
                    var year = d.substring(0,4);
				    if (!(i % 4)) return year;
                }else{
                    return ""
                }
		
			})
			)
            .select(".domain").remove()
        // Customization

        svg_stream.selectAll(".tick line")
        .attr("stroke", "grey")
        if(level == "category"){
            svg_stream.selectAll(".tick line")
            .attr("stroke-opacity", 0.8);
        }


			
		svg_stream_2.selectAll(".tick line")
        .attr("stroke", "grey")
        if(level == "category"){
            svg_stream.selectAll(".tick line")
            .attr("stroke-opacity", 0.8);
        }
		
		if(ticksEnabled){
            // Add X axis label:
            svg_stream_2.append("text")
                .attr("text-anchor", "end")
                .attr("x", width_stream_graph)
                .attr("y", height_stream_graph -3 )
                .attr('font-size', 12)
                .text("Year");
        }
		


        //stack the data?
     
        var stackedData = d3.stack().keys(keys)(data)


        // Area generator
        var area = d3.area()
            .x(function(d) {return x(d.data.time_step_graph); })
            .y0(function(d) { return y(d[0]); })
            .y1(function(d) {return y(d[1]); })

        // create a tooltip
        var Tooltip = svg_stream
            .append("text")
            .attr("x", 0)
            .attr("y", 20)
            .style("opacity", 0)
            .style("font-size", 17)
        
        var mouseover = function(d) {
            Tooltip.style("opacity", 1)
            d3.selectAll(".myArea-" + level ).style("opacity", .2)
            d3.select(this)
            .style("opacity", 1)
                d3.selectAll(".myArea-" + level )            
                .style("stroke", "black")

                 
        }
        var mousemove = function(d,i) {
            grp = d.key
            Tooltip.text(grp)
 
        }
        var mouseleave = function(d) {
            Tooltip.style("opacity", 0)
            d3.selectAll(".myArea-" + level ).style("opacity", 1)
            d3.selectAll(".myArea-category" ).style("stroke", "none")
            
            
        }

        function logLenSelection(d){
        }

        var clickedStream = function(d){
            current_date = invertX(d3.mouse(this)[0])
            current_date_ind = validTimeSteps_graph.findIndex((element) => element == current_date)
            updateStreamSlider()
        }

        var clickedStreamFocused = function(d){
            document.getElementById("filterInput").value = d.key
            filterTagsByString()
        }

        var clickFunction = level == "category"?clickedStream:clickedStreamFocused
        
                var p = svg_stream.selectAll(".myArea-" + level)
                    .data(stackedData, function(d) {
                        return d.key;
                    })


                p.enter()   
                .call(logLenSelection)         
                .append("path")
                .attr("id", function(d){return "path-" + d.key})
                
                .attr("class", "myArea-" + level )

                .attr("d", area)

                .on("mouseover", mouseover)
                .on("mousemove", mousemove)
                .on("mouseleave", mouseleave)
                .on("click", clickFunction)


                    .merge(p)
                    .transition()
                    .duration(750)
                    .attr("d", area)
                    .style("fill", function(d) { 
                    
                    if(filterString != null){
           
                        return myColor(filterCategory)
                    }
                    else if(!d){
                    return 'grey'
                    }
                    else if(level == "tag"){
                        return myColor(reverseTagCatIndex[d.key]) 
                    }else{
                        return myColor(d.key)
                    }
                })
                p.exit()
                .remove()
                

   
        d3.selectAll(".myArea-tag" )            
                .style("stroke", "black")
                .attr('stroke-width', .2)
		

		
    }



    function updateStreamSlider(){
        var rectGrabBottom = height 
        var rectGrabTop = height - height_stream_2 - height_stream +2
        var focusRectCornerTop = height + height_stream + 15
        var focusRectCornerRight = x_main_stream(current_date) + (rectWidthRight)
        var focusRectCornerLeft = x_main_stream(current_date) - (rectWidthLeft)

        d3.select("#sliderG").remove()
        d3.selectAll("#line-focus").remove()


        var sliderG = d3.select("#streamContainer").append("g").attr("id", "sliderG")
        .attr("transform",
            "translate(" + 20 + "," + 150 + ")")
        .data([{x: sliderGPosX, y: 0}]);

		var lineCol0or = '#5e5e5e'
		
        sliderG
            .append("line")
            .attr('id', "line-comparison")
            .attr('stroke', lineCol0or)
            .attr('stroke-width', 1)
            .attr('x1', x_main_stream(current_date))
            .attr('y1', rectGrabBottom )
            .attr('x2', x_main_stream(current_date))
            .attr('y2', rectGrabTop)
            .call(drag);

        sliderG
            .append("line")
            .attr('id', "line-split")
            .attr('stroke', lineCol0or)
            .attr('stroke-width', 0.5)
            .attr('x1', focusRectCornerLeft)
            .attr('y1', height - height_stream + 5)
            .attr('x2', focusRectCornerRight)
            .attr('y2', height - height_stream + 5 )
        sliderG
            .append("rect")
            .attr('id', "rect-grab")
            .style("fill", "black")
            .attr("fill-opacity","0.05")
            .attr("rx", 3)
            .attr("ry", 3)
            .style("stroke", lineCol0or)
			.style("stroke-opacity", 1)
            .attr("width", focusRectCornerRight - focusRectCornerLeft)
            .attr("height",  rectGrabBottom - rectGrabTop )
            .attr("x", focusRectCornerLeft)
            .attr("y", rectGrabTop)
            .call(drag);
		
		
        /// magnifying lines to left
        main_container
            .append("line")
            .attr('id', "line-focus")
            .attr('stroke', 'grey')
            .attr('stroke-width', 2)
            .style("stroke-dasharray", ("3, 3"))
            .attr('x1', focusRectCornerLeft + width_side_panel + margin.left)
            .attr('y1', focusRectCornerTop)
            .attr('x2', focusStremTartgetLeft)
            .attr('y2', focusStremTartgetTop)
            .call(drag);
        main_container
            .append("line")
            .attr('id', "line-focus")
            .attr('stroke', 'grey')
            .attr('stroke-width', 2)
            .style("stroke-dasharray", ("3, 3"))
            .attr('x1', focusRectCornerRight + width_side_panel + margin.left)
            .attr('y1', focusRectCornerTop)
            .attr('x2', focusStremTartgetRight)
            .attr('y2', focusStremTartgetTop)
            .call(drag);

        /// magnifying lines to right
        main_container
            .append("line")
            .attr('id', "line-focus")
            .attr('stroke', '#E3E3E3')
            .attr('stroke-width', 2)
            .style("stroke-dasharray", ("3, 3"))
            .attr('x1', focusRectCornerLeft + width_side_panel + margin.left)
            .attr('y1', focusRectCornerTop + height_stream - rectAdd)
            .attr('x2', focusStremTartgetLeft + width + width_side_panel - focusMargin)
            .attr('y2', focusStremTartgetTop)
            .call(drag);
        main_container
            .append("line")
            .attr('id', "line-focus")
            .attr('stroke', 'grey')
            .attr('stroke-width', 2)
            .style("stroke-dasharray", ("3, 3"))
            .attr('x1', focusRectCornerRight + width_side_panel + margin.left)
            .attr('y1', focusRectCornerTop+ height_stream - rectAdd)
            .attr('x2', focusStremTartgetRight  + width + width_side_panel- focusMargin)
            .attr('y2', focusStremTartgetTop)
            .call(drag);
		
		
		var grabberHeight = 20
		var grabberWidth = 25
        /// add draggable rect to adjust size of focus window
        sliderG
            .append("rect")
            .attr('id', "focus-grab")
            .attr("width",grabberWidth)
            .attr("height", grabberHeight)
            .attr("x", focusRectCornerLeft - 15)
            .attr("y", height - height_stream -4)
            .call(dragLeft);
			
        sliderG
            .append("rect")
            .attr('id', "focus-grab")
            .attr("width", grabberWidth)
            .attr("height", grabberHeight)
            .attr("x", focusRectCornerRight-10)
            .attr("y", height - height_stream -4 )
            .call(dragRight);
			
		sliderG
			.append("text").text( "<>")
			.attr('id', "focus-grab-text")
			.attr("x", focusRectCornerRight-6)
            .attr("y", height - height_stream +10 );
			
		sliderG
			.append("text").text( "<>")
			.attr('id', "focus-grab-text")
            .attr("x", focusRectCornerLeft - 12)
            .attr("y", height - height_stream +10)
			
		

        //calling update on map
        current_year_data = countries_mock_data.timesteps[current_date];

        draw(world_countries ,current_year_data)
        
        refreshStreamGraph(country_in_focus_1, left_focus_g, getFocusedValidSteps(), width_stream_focused, height_stream_focused, "tag")
        refreshStreamGraph(country_in_focus_2, right_focus_g, getFocusedValidSteps(), width_stream_focused, height_stream_focused, "tag")
        updatedMultiDonut(country_in_focus_1, getFocusedValidSteps());
        updatedMultiDonutRight(country_in_focus_2, getFocusedValidSteps());
          
    }


