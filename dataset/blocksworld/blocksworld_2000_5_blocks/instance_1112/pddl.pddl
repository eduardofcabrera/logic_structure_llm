

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(ontable b)
(on c b)
(on d e)
(on e a)
(clear d)
)
(:goal
(and
(on b a)
(on c b)
(on d e)
(on e c))
)
)


