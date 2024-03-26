

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b c)
(ontable c)
(on d b)
(ontable e)
(clear a)
(clear d)
)
(:goal
(and
(on b d)
(on c b)
(on d e)
(on e a))
)
)


