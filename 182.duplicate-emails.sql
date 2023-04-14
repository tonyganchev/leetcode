--
-- @lc app=leetcode id=182 lang=mysql
--
-- [182] Duplicate Emails
--

-- @lc code=start
# Write your MySQL query statement below

select distinct p1.email
from person p1
inner join person p2 on p1.email = p2.email and p1.id <> p2.id

-- @lc code=end

