"""Object Representation of Schematic"""

from typing import List,Tuple,Set

class Schematic:
    def __init__(self,schematic_input:List[List[str]]):
        self.dataset = schematic_input
        self.pointer_x=0
        self.pointer_y=0

    @property
    def width(self):
        return len(self.dataset[0])
    
    @property
    def length(self):
        return len(self.dataset)
    
    def gear_ratio_total(self)->int:
        """Return sum of all gear ratios"""
        valid_gears = self.gear_ratios()
        gear_ratios_calculated = []
        for a,b in valid_gears:
            gear_ratios_calculated.append(a*b)

        return sum(gear_ratios_calculated)

    def gear_ratios(self)->List:
        """Return List of all gear_ratios"""
        part_number_areas = self._find_part_numbers()[1]
        gears = {} #Tuple of location of gear, list of values touching
        for part_number_area in part_number_areas:
            gear_locations = self._get_gear_locations_for_area(part_number_area)
            if gear_locations is not None:
                for gear in gear_locations:
                    if gear in gears:
                        gears[gear].append(self._convert_area_to_number(part_number_area))
                    else:
                        gears[gear]=[self._convert_area_to_number(part_number_area)]
        valid_gears = []
        for gear in gears.values():
            if len(gear)==2:
                valid_gears.append(gear)
        return valid_gears


    def _get_gear_locations_for_area(self,area:List)->Set[Tuple[int]]:
        """Returns location of gear or None """
        gears = set()
        for point in area:
            gears.update(self._get_gear_locations_for_point(point))
        return gears

    def _get_gear_locations_for_point(self,point:Tuple)-> Set[Tuple[int]]:
        """Returns location of gear or None"""
        x,y=point
        adjacencies = [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
        gears=set()
        for x_check, y_check in adjacencies:
            if 0<=x_check<self.width and 0<=y_check<self.length:
                if self._is_star((x_check,y_check)):
                    gears.add((x_check,y_check))
        return gears   





    def part_number_total(self):
        """Return Sum of all part numbers"""
        return sum(self._find_part_numbers()[0])
    
    
    def _find_part_numbers(self)-> Tuple[List[int],List[Tuple]]:
        """Return list of all part numbers"""
        part_numbers = []
        part_number_areas = []
        possible_part_number_area= self._get_next_number_area()
        while possible_part_number_area:
            if self._is_part_number(possible_part_number_area):
                part_numbers.append(int(self._convert_area_to_number(possible_part_number_area)))
                part_number_areas.append(possible_part_number_area)
            possible_part_number_area= self._get_next_number_area()
        return part_numbers,part_number_areas
            
    def _increment_pointer(self)->int:
        """Increments pointer ensuring it doesn't go out of bounds
        Uses the following return codes:
        0 = OK
        1 = End of Line Reached
        2 = End of Array Reached
        """
        x=self.pointer_x
        y=self.pointer_y
        result=0
        y+=1
        if y==self.width:
            y=0
            x+=1
            result+=1
            if x==self.length:
                x=0
                result+=1
        self.pointer_x=x
        self.pointer_y=y
        return result

    def _get_next_number_area(self)->List[Tuple]:
        """Return next valid part number in schematic"""
        area = []
        while not self.dataset[self.pointer_x][self.pointer_y].isnumeric():
            if self._increment_pointer()==2:
                return []
        while self.dataset[self.pointer_x][self.pointer_y].isnumeric():
            area.append((self.pointer_x,self.pointer_y))
            if self._increment_pointer()>0:
                return area
        return area

    def _convert_area_to_number(self,area:List[Tuple])->int:
        """Return an integer indicated by list of Tuples"""
        number= ""
        for x,y in area:
            number+=self.dataset[x][y]
        return int(number)
    
    def _is_part_number(self,area:List[Tuple])->bool:
        """Return True if indicated number is part number"""
        for point in area:
            if self._has_adjacent_symbol(point):
                return True
        return False

    def _has_adjacent_symbol(self, position:Tuple[int,int])->bool:
        """Return true if location has an adjacent symbol"""
        x,y=position
        adjacencies = [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
        for x_check, y_check in adjacencies:
            if 0<=x_check<self.width and 0<=y_check<self.length:
                if self._is_symbol((x_check,y_check)):
                    return True
        return False
    
    def _is_star(self, position)->bool:
        """Return true if location contains an asterisk"""
        x,y=position
        return self.dataset[x][y]=="*"


    def _is_symbol(self,position)->bool:
        """Returns true if location contains a symbol"""
        x,y=position
        if self.dataset[x][y].isnumeric():
            return False
        if self.dataset[x][y]==".":
            return False
        return True



